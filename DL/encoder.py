import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras import regularizers
from tensorflow.keras.optimizers import Adam

# 加载数据集
data = pd.read_csv('kddcup.data_10_percent_corrected', header=None)

# 数据预处理
# 选择特征列和标签列
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# 将标签转换为0和1，其中0表示正常流量，1表示异常流量
y = np.where(y == 'normal.', 0, 1)

# 标准化数据
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 将数据分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 构建Autoencoder模型
input_dim = X_train.shape[1]
encoding_dim = 14

input_layer = Input(shape=(input_dim,))
encoder = Dense(encoding_dim, activation="tanh", activity_regularizer=regularizers.l1(10e-5))(input_layer)
encoder = Dense(int(encoding_dim / 2), activation="relu")(encoder)
decoder = Dense(int(encoding_dim / 2), activation='tanh')(encoder)
decoder = Dense(input_dim, activation='relu')(decoder)
autoencoder = Model(inputs=input_layer, outputs=decoder)

# 编译模型
autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error', metrics=['accuracy'])

# 训练模型
history = autoencoder.fit(X_train, X_train, epochs=100, batch_size=256, shuffle=True, validation_split=0.2, verbose=1)

# 保存模型
autoencoder.save('autoencoder_model.h5')
