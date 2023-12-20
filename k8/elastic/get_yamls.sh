# export ECK_VERSION=current
export ECK_VERSION=2.10.0

curl https://download.elastic.co/downloads/eck/${ECK_VERSION}/crds.yaml -O
curl https://download.elastic.co/downloads/eck/${ECK_VERSION}/operator.yaml -O

