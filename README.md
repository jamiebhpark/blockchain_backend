### **Blockchain Asset Trader Portfolio**

## Introduction

Welcome to my Blockchain Asset Trader project. This project demonstrates my proficiency in SwiftUI for iOS app development and Flask for backend development, integrating blockchain technology using Web3 and the Ethereum network. The primary goal of this project is to allow users to register, log in, send transactions, and check their Ethereum asset balance seamlessly.

---

## Features

### 1. User Authentication

- **Register**: Users can register with a username, password, and Ethereum address.
- **Login**: Secure login functionality with JWT authentication.

### 2. Transaction Management

- **Send Transaction**: Users can send Ethereum transactions to any Ethereum address.
- **View Transactions**: Users can view the list of transactions they have sent and received.
- **Transaction Detail**: Detailed view of each transaction, including sender, receiver, amount, timestamp, and transaction hash.

### 3. Asset Management

- **Check Assets**: Users can check their current asset balance and Ethereum balance.

### 4. Real-time Notifications

- **Push Notifications**: The app requests notification permissions and handles basic notification alerts.

---

## Screenshots

1. Dashboard
    
    ![IMG_4896.PNG](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9f35de7-0091-4a79-819a-501ef9435828/61b08d3c-2f70-44fa-8331-8150fd540508/IMG_4896.png)
    
2. Register
    
    ![IMG_4897.PNG](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9f35de7-0091-4a79-819a-501ef9435828/737efce1-735c-40c0-8cff-b6708887b20e/IMG_4897.png)
    
3. Login
    
    ![IMG_4898.PNG](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9f35de7-0091-4a79-819a-501ef9435828/81817c2f-8954-44e6-9670-62d179d3f60f/IMG_4898.png)
    
4. Send Transaction
    
    ![IMG_4904.JPG](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9f35de7-0091-4a79-819a-501ef9435828/5ca52c2e-57cd-43e7-b575-b732fa8a842d/IMG_4904.jpg)
    
5. Transaction List
    
    ![IMG_4905.JPG](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9f35de7-0091-4a79-819a-501ef9435828/65987b35-4c1f-492b-ad64-e70e51582339/IMG_4905.jpg)
    
6. Transaction Detail
    
    ![IMG_4901.PNG](https://prod-files-secure.s3.us-west-2.amazonaws.com/f9f35de7-0091-4a79-819a-501ef9435828/6ada0fdd-4cd2-48fe-b8d5-a7e9de418373/IMG_4901.png)
    

---

## Technologies Used

### Frontend

- **SwiftUI**: Modern UI framework for building declarative UI for iOS.
- **UserNotifications**: Framework for handling notifications in iOS.

### Backend

- **Flask**: A lightweight WSGI web application framework in Python.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Web3.py**: Python library for interacting with Ethereum.
- **JWT**: JSON Web Tokens for secure user authentication.

### Blockchain

- **Ethereum**: Public blockchain network.
- **Infura**: Ethereum node service provider.

---

## Code Highlights

### Frontend (iOS - SwiftUI)

**App Entry Point (BlockChainAssetTraderApp.swift)**

```swift
import SwiftUI

@main
struct BlockChainAssetTraderApp: App {
    @StateObject private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
        }
    }
}

```

**ContentView**

```swift
import SwiftUI
import UserNotifications

struct ContentView: View {
    @EnvironmentObject var appState: AppState

    init() {
        // 알림 권한 요청
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { granted, error in
            if granted {
                print("Notification permission granted.")
            } else if let error = error {
                print("Notification permission denied because: \\(error.localizedDescription)")
            }
        }
    }

    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                Text("Welcome to Blockchain Asset Trader")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .multilineTextAlignment(.center)
                    .padding()

                Spacer()

                NavigationLink(value: NavigationDestination.register) {
                    HStack {
                        Image(systemName: "person.crop.circle.badge.plus")
                        Text("Register")
                            .fontWeight(.semibold)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }
                .padding(.horizontal, 16)

                NavigationLink(value: NavigationDestination.login) {
                    HStack {
                        Image(systemName: "person.crop.circle")
                        Text("Login")
                            .fontWeight(.semibold)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.green)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }
                .padding(.horizontal, 16)

                NavigationLink(value: NavigationDestination.transaction) {
                    HStack {
                        Image(systemName: "arrow.up.arrow.down.circle")
                        Text("Send Transaction")
                            .fontWeight(.semibold)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.orange)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }
                .padding(.horizontal, 16)

                NavigationLink(value: NavigationDestination.assets) {
                    HStack {
                        Image(systemName: "creditcard.circle")
                        Text("Check Assets")
                            .fontWeight(.semibold)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.purple)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }
                .padding(.horizontal, 16)

                NavigationLink(value: NavigationDestination.transactionList) {
                    HStack {
                        Image(systemName: "list.bullet")
                        Text("View Transactions")
                            .fontWeight(.semibold)
                    }
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.gray)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }
                .padding(.horizontal, 16)

                Spacer()
            }
            .padding()
            .navigationTitle("Dashboard")
            .navigationBarTitleDisplayMode(.inline)
            .navigationDestination(for: NavigationDestination.self) { destination in
                switch destination {
                case .register:
                    RegisterView()
                case .login:
                    LoginView()
                case .transaction:
                    TransactionView()
                case .assets:
                    AssetView()
                case .transactionDetail(let transaction):
                    TransactionDetailView(transaction: transaction)
                case .transactionList:
                    TransactionListView()
                }
            }
        }
    }
}

```

**TransactionDetailView**

```swift
import SwiftUI

struct TransactionDetailView: View {
    var transaction: BlockchainTransaction

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Transaction Details")
                .font(.largeTitle)
                .padding(.bottom, 20)

            Text("Sender: \\(transaction.sender)")
            Text("Receiver: \\(transaction.receiver)")
            Text("Amount: \\(transaction.amount)")
            Text("Timestamp: \\(transaction.timestamp)")
            Text("Transaction Hash: \\(transaction.txn_hash)")
                .padding(.top, 20)

            Spacer()
        }
        .padding()
        .navigationTitle("Transaction Detail")
    }
}

```

**TransactionListView**

```swift
import SwiftUI

struct TransactionListView: View {
    @EnvironmentObject var appState: AppState
    @State private var transactions: [BlockchainTransaction] = []
    @State private var message: String = ""

    var body: some View {
        VStack {
            if transactions.isEmpty {
                Text(message)
                    .foregroundColor(.red)
                    .padding()
            } else {
                List(transactions) { transaction in
                    VStack(alignment: .leading) {
                        Text("Sender: \\(transaction.sender)")
                        Text("Receiver: \\(transaction.receiver)")
                        Text("Amount: \\(transaction.amount)")
                        Text("Timestamp: \\(transaction.timestamp)")
                    }
                }
            }
        }
        .navigationTitle("Transaction List")
        .onAppear {
            fetchTransactions()
        }
    }

    func fetchTransactions() {
        guard let url = URL(string: "\\(serverURL)/transactions") else { return }
        var request = URLRequest(url: url)
        request.setValue(appState.token, forHTTPHeaderField: "x-access-token")

        URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data else {
                DispatchQueue.main.async {
                    self.message = "Failed to fetch transactions."
                }
                return
            }
            if let transactions = try? JSONDecoder().decode([BlockchainTransaction].self, from: data) {
                DispatchQueue.main.async {
                    self.transactions = transactions
                }
            } else {
                DispatchQueue.main.async {
                    self.message = "Failed to fetch transactions."
                }
            }
        }.resume()
    }
}

```

### Backend (Flask)

[**app.py**](http://app.py/)

```python
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
            data = jwt

.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
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

@app.route('/eth_balance', methods=['GET'])
@token_required
def get_eth_balance(current_user):
    user = User.query.filter_by(username=current_user).first()
    ethereum_address = user.ethereum_address
    balance = web3.eth.get_balance(ethereum_address)
    eth_balance = web3.from_wei(balance, 'ether')
    return jsonify({"eth_balance": str(eth_balance)}), 200

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

```

[**models.py**](http://models.py/)

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    ethereum_address = db.Column(db.String(120), unique=True, nullable=False)
    assets = db.Column(db.Float, default=1000.0)

class Transaction(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    receiver = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    txn_hash = db.Column(db.String(120), nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat(),
            "txn_hash": self.txn_hash
        }

```

---

## Testing Scenarios

1. **User Registration**
    - Open the app and navigate to the "Register" screen.
    - Enter a username, password, and Ethereum address, then press "Register".
    - Verify that the registration is successful.
2. **User Login**
    - Navigate to the "Login" screen.
    - Enter the registered username and password, then press "Login".
    - Verify that the login is successful and a token is generated.
3. **Send Transaction**
    - Navigate to the "Send Transaction" screen.
    - Enter a valid Ethereum address and an amount, then press "Send Transaction".
    - Verify that the transaction is sent successfully and appears in the transaction list.
4. **View Transactions**
    - Navigate to the "View Transactions" screen.
    - Verify that the transactions are listed correctly with all details.
5. **Check Assets**
    - Navigate to the "Check Assets" screen.
    - Press "Check Assets" and verify that the correct balance and Ethereum balance are displayed.
6. **Check Ethereum Balance**
    - Verify that the correct Ethereum balance is fetched and displayed.

---

## Conclusion

This project demonstrates a full-stack blockchain application integrating iOS development with SwiftUI and backend development with Flask, showcasing proficiency in modern technologies and the ability to create a seamless user experience with blockchain integration.

Thank you for reviewing my project!
