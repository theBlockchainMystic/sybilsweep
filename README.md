docker build --tag sybil-docker .
docker run -d -p 5000:5000 sybil-docker

Steps involved in the Exploratory Data Analysis of the Fantom and Unicef voting data

Step 1: Standardizing the amount column based on the token, and calculating the time difference between transactions for a destination wallet paid in respective tokens.

Standardizing the amount column based on the token and calculating the time difference between transactions for a destination wallet paid in respective tokens is important because it allows for more accurate analysis of cryptocurrency transactions.

Standardizing the amount column ensures that all amounts are in the same unit (e.g. all amounts are in BTC, or all amounts are in ETH), which makes it easier to compare and analyze the data. Without standardizing, it would be difficult to compare transactions that are denominated in different tokens because the value of each token can fluctuate over time.

Calculating the time difference between transactions for a destination wallet paid in respective tokens allows for analysis of the frequency of transactions and patterns in the movement of funds. This information can be used to identify potential illicit activity, such as money laundering or illegal activity, or to identify legitimate use cases such as recurring payments or salary payments.

Overall, standardizing the amount column and calculating the time difference between transactions can provide valuable insights into the movement of funds on a blockchain, which can be used for a variety of purposes such as detecting fraudulent activity, identifying legitimate use cases, and understanding the overall health and usage of the blockchain network.

Step 2: Visualizing the standardized amount and time difference using boxplots.

Visualizing the standardized amount and time difference using boxplots is important because it allows for the detection of outliers and anomalies in the data, which can indicate suspicious or fraudulent activity. Boxplots also provide a clear and easy-to-understand representation of the distribution of the data, making it easier to identify patterns and trends. Additionally, boxplots can help to identify the average and median values of the data, which can be useful in determining normal behavior. Overall, visualizing the data in this way can aid in detecting and analyzing potential issues, and can provide valuable insights for further investigation.

Step 3: Training two machine learning models for anomaly detection: Isolation Forest and Robust Covariance.

Training machine learning models for anomaly detection is important because it allows you to identify patterns in your data that deviate from the norm, which may indicate the presence of sybils. The Isolation Forest and Robust Covariance algorithms are both commonly used for anomaly detection and can help identify sybils by detecting patterns in the standardized amount and time difference data.

Isolation Forest is based on the decision tree algorithm and uses the concept of isolation to identify anomalies. This algorithm can identify anomalies by randomly selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature, and this way it can isolate the observations which are different from the rest of the observations.

Robust Covariance is an algorithm that is robust to outliers, it can estimate the covariance matrix in the presence of outliers, it's an alternative to the traditional MLE algorithm, which is sensitive to outliers. This algorithm can be used to detect the presence of sybils by identifying patterns in the data that deviate from the norm.

![Outlier detection across models](../Oulier ratio.png "Outlier detection")

It's important to note that using multiple machine learning models to detect sybils can increase the accuracy of the detection, as different models can identify different patterns in the data.

Step 4: Saving the trained models to files and loading them to be used later.

Saving the trained models to files and loading them later is important because it allows the models to be used again in the future without the need to retrain them. This can save a significant amount of time and computational resources. Additionally, saving the models to files allows them to be shared and used by other people or systems. This is especially useful when working in a team or when the models are used in production environments. The models can be loaded and used again whenever necessary, without the need to retrain them every time.

Step 5: The Isolation Forest model returns an anomaly score for an input sample, computed as the mean anomaly score of the trees in the forest. The measure of normality of an observation given a tree is the depth of the leaf containing this observation.

The Isolation Forest algorithm is an unsupervised machine learning method for anomaly detection. It works by creating a decision tree structure where each node represents a sample in the dataset and each leaf represents a partition of the sample space. The algorithm isolates observations by randomly selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature. The goal of this process is to split the data into smaller and smaller partitions, eventually isolating individual observations.

The model returns an anomaly score for an input sample, computed as the mean anomaly score of the trees in the forest. The anomaly score is the number of steps required to isolate the sample in the tree structure, also known as the path length. The smaller the path length, the more abnormal the observation is.

The measure of normality of an observation given a tree is the depth of the leaf containing this observation. The depth of the leaf gives an idea about how isolated the observation is. The deeper the leaf, the more isolated the observation is and the more abnormal it is considered to be.

Isolation Forest is useful for detecting sybils in this dataset because it is a model-based method which can identify outliers or abnormal observations by considering the entire dataset and not just individual features. It is also efficient for high-dimensional datasets as it doesn't require feature scaling and is robust to irrelevant and noisy features.

Step 6: The Robust Covariance model returns a Mahalanobis distance which is a statistical metric that measures how far an observation is from the center of the distribution. Outliers fall farther away from the center and thus have a higher Mahalanobis distance.

The Robust Covariance model is a statistical technique that is used to identify outliers in a dataset. It is based on the Mahalanobis distance, which is a measure of how far an observation is from the center of the distribution of the data. This is important for detecting sybils in the dataset because sybils are typically defined as being outliers or anomalies in the data. The Mahalanobis distance allows us to identify observations that are unusually far from the center of the distribution, which may indicate that they are sybils.

The Mahalanobis distance is calculated by taking the difference between an observation and the mean of the distribution, and then multiplying that difference by the inverse of the covariance matrix of the distribution. This results in a number that represents how far an observation is from the center of the distribution in terms of standard deviations. Observations that are farther away from the center of the distribution will have a higher Mahalanobis distance and are more likely to be considered outliers or sybils.

In this dataset, the Robust Covariance model can be used to detect sybils by identifying transactions that have a Mahalanobis distance that is significantly higher than the rest of the transactions. These transactions are likely to be sybils and can be flagged for further investigation.
