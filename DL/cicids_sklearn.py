import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# 读取数据集
file_list = [
    'TrafficLabelling/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv',
    'TrafficLabelling/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv',
    'TrafficLabelling/Friday-WorkingHours-Morning.pcap_ISCX.csv',
    'TrafficLabelling/Monday-WorkingHours.pcap_ISCX.csv',
    'TrafficLabelling/Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv',
    'TrafficLabelling/Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv',
    'TrafficLabelling/Tuesday-WorkingHours.pcap_ISCX.csv',
    'TrafficLabelling/Wednesday-workingHours.pcap_ISCX.csv'
]

data_frames = []
for file in file_list:
    try:
        df = pd.read_csv(file, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(file, encoding='latin1')
        except UnicodeDecodeError:
            df = pd.read_csv(file, encoding='ISO-8859-1')
    data_frames.append(df)

# 合并数据集
data = pd.concat(data_frames, ignore_index=True)

# 显示数据集信息
print("数据集总行数:", len(data))
print("数据集列名:", data.columns)

# 选择一些重要特征作为输入
features = [
    'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
    'Fwd Packet Length Mean', 'Bwd Packet Length Mean', 'Flow Bytes/s',
    'Flow Packets/s', 'Fwd IAT Mean', 'Bwd IAT Mean', 'Fwd PSH Flags',
    'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length',
    'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Std',
    'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count',
    'PSH Flag Count', 'ACK Flag Count', 'URG Flag Count', 'CWE Flag Count',
    'ECE Flag Count', 'Down/Up Ratio', 'Average Packet Size', 'Avg Fwd Segment Size',
    'Avg Bwd Segment Size', 'Init_Win_bytes_forward', 'Init_Win_bytes_backward', 'act_data_pkt_fwd'
]
# 确保所有特征列在数据集中存在
missing_features = [feature for feature in features if feature not in data.columns]
if missing_features:
    print(f"缺少的特征列: {missing_features}")
else:
    print("所有特征列都存在")


X = data[features]

# 将标签转换为二进制分类（正常和攻击）
label_encoder = LabelEncoder()
data['Label'] = label_encoder.fit_transform(data['Label'])
y = data['Label']

# 分割训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 标准化特征
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 保存标准化模型
import joblib
joblib.dump(scaler, 'scaler.pkl')

# 将数据处理为时间序列格式
def create_sequences(data, seq_length):
    sequences = []
    for i in range(len(data) - seq_length):
        sequences.append(data[i:i+seq_length])
    return np.array(sequences)

seq_length = 10
X_train_seq = create_sequences(X_train, seq_length)
X_test_seq = create_sequences(X_test, seq_length)
y_train_seq = y_train[seq_length:]
y_test_seq = y_test[seq_length:]

# 构建LSTM模型
lstm_model = models.Sequential([
    layers.LSTM(64, input_shape=(seq_length, X_train_seq.shape[2]), return_sequences=True),
    layers.LSTM(32),
    layers.Dense(1, activation='sigmoid')
])

lstm_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 训练模型
lstm_model.fit(X_train_seq, y_train_seq, epochs=20, batch_size=32, validation_split=0.2)

# 保存模型
lstm_model.save('lstm_model.h5')

# 评估模型
test_loss, test_acc = lstm_model.evaluate(X_test_seq, y_test_seq)
print(f'测试集准确率: {test_acc:.2f}')