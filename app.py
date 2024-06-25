# app.py
from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
import uuid
import jwt
from functools import wraps
from web3 import Web3
from dotenv import load_dotenv
import os
from models import db, User, Transaction

# .env 파일 로드
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # JWT 시크릿 키 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Infura를 통해 Sepolia 테스트넷 노드에 연결
infura_url = os.getenv('INFURA_URL')
web3 = Web3(Web3.HTTPProvider(infura_url))

# 환경 변수에서 개인 키 가져오기
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
if not PRIVATE_KEY:
    raise ValueError("PRIVATE_KEY is not set in environment variables")

# 개인 키에 해당하는 이더리움 주소 가져오기
PRIVATE_KEY_ADDRESS = web3.eth.account.from_key(PRIVATE_KEY).address

# Debugging information
print(f"PRIVATE_KEY_ADDRESS: {PRIVATE_KEY_ADDRESS}")


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(current_user, *args, **kwargs)

    return decorator


def create_blockchain_transaction(sender, receiver, amount):
    try:
        gas_price = web3.to_wei('1', 'gwei')  # 가스 가격을 1 gwei로 설정
        gas_limit = 21000  # 일반 트랜잭션을 위한 가스 한도
        tx_cost = gas_limit * gas_price
        total_cost = tx_cost + web3.to_wei(amount, 'ether')
        balance = web3.eth.get_balance(sender)

        if balance < total_cost:
            print(f"Error: Insufficient funds. Balance: {balance}, Required: {total_cost}")
            return None

        transaction = {
            'from': sender,
            'to': receiver,
            'value': web3.to_wei(amount, 'ether'),
            'gas': gas_limit,
            'gasPrice': gas_price,
            'nonce': web3.eth.get_transaction_count(sender),
        }
        print(f"Transaction: {transaction}")
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return txn_hash.hex()
    except Exception as e:
        print(f"Error in create_blockchain_transaction: {e}")
        return None


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    ethereum_address = data.get('ethereum_address')
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "User already exists"}), 400
    user = User(username=username, password=password, ethereum_address=ethereum_address)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user is None:
        return jsonify({'message': 'Invalid username or password'}), 401

    token = jwt.encode({'username': username, 'exp': datetime.now(timezone.utc) + timedelta(minutes=30)},
                       app.config['SECRET_KEY'])
    return jsonify({'token': token})


@app.route('/transaction', methods=['POST'])
@token_required
def create_transaction(current_user):
    data = request.get_json()
    print(f"Received data: {data}")
    sender = current_user
    receiver = data.get('receiver')
    amount = data.get('amount')

    if not sender or not receiver or not amount:
        print(f"Error: Missing data: sender={sender}, receiver={receiver}, amount={amount}")
        return jsonify({"error": "Missing data"}), 400

    user = User.query.filter_by(username=sender).first()
    if user is None:
        print(f"Error: User does not exist: sender={sender}")
        return jsonify({"error": "User does not exist"}), 400
    if user.assets < float(amount):
        print(f"Error: Insufficient assets: sender={sender}, assets={user.assets}, amount={amount}")
        return jsonify({"error": "Insufficient assets"}), 400

    sender_ethereum_address = user.ethereum_address

    # 블록체인 트랜잭션 생성
    txn_hash = create_blockchain_transaction(sender_ethereum_address, receiver, amount)
    if not txn_hash:
        print(f"Error: Failed to create blockchain transaction")
        return jsonify({"error": "Failed to create blockchain transaction"}), 400

    user.assets -= float(amount)
    receiver_user = User.query.filter_by(ethereum_address=receiver).first()
    if receiver_user:
        receiver_user.assets += float(amount)
    transaction_record = Transaction(
        id=str(uuid.uuid4()),
        sender=sender,
        receiver=receiver,
        amount=amount,
        timestamp=datetime.now(timezone.utc),
        txn_hash=txn_hash
    )
    db.session.add(transaction_record)
    db.session.commit()

    return jsonify({"message": "Transaction successful", "txn_hash": txn_hash}), 201


@app.route('/transactions', methods=['GET'])
@token_required
def get_transactions(current_user):
    user_transactions = Transaction.query.filter(
        (Transaction.sender == current_user) | (Transaction.receiver == current_user)
    ).all()
    return jsonify([t.as_dict() for t in user_transactions]), 200


@app.route('/assets', methods=['GET'])
@token_required
def get_assets(current_user):
    user = User.query.filter_by(username=current_user).first()
    return jsonify({"assets": user.assets}), 200


def calculate_transaction_cost():
    gas_price = web3.to_wei('1', 'gwei')
    gas_limit = 21000
    transaction_cost = gas_price * gas_limit
    return web3.from_wei(transaction_cost, 'ether')


print(f"PRIVATE_KEY_ADDRESS: {PRIVATE_KEY_ADDRESS}")
print(f"Estimated transaction cost: {calculate_transaction_cost()} ETH")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 데이터베이스 테이블 생성
    app.run(host='0.0.0.0', port=5001, debug=True)
