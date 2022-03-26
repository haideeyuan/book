for i in p_data:
  for j in c_data:
    gmx_md_flow(p_data, c_data, conf)

    
## 卷积层 ##
W_conv2 = weight_variable([5,5, 32, 64]) 
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
## 池化层 ##
h_pool2 = max_pool_2x2(h_conv2)

## 全连接层 ##
W_fc1 = weight_variable([7*7*64, 1024])
b_fc1 = bias_variable([1024])
## Dropout层 ##
h_fc1_drop = tf.nn.dropout(b_fc1, keep_prob)
