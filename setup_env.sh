export CARO_LOGFILE=caro.log
export CARO_FOLDER=$(pwd)
export CARO_CAPTURE_FOLDER=$CARO_FOLDER/client/capture/
export CARO_INBOX_FOLDER=$CARO_FOLDER/server/inbox/

export CARO_CLOUD_CONFIG_FILE=clouds.yaml

export CARO_CLOUD_NAME=eams_cloud
export CARO_CLOUD_INSTANCE_NAME=DARKNET-1
export CARO_CLOUD_INSTANCE_IMAGE=None
export CARO_CLOUD_INSTANCE_FLAVOR=m1.compute
export CARO_CLOUD_INSTANCE_BOOT_VOLUME=6a2d16fd-2914-463e-8c13-adf51b1c89ca
export CARO_CLOUD_INSTANCE_BOOT_VOLUME_SIZE=10
export CARO_CLOUD_INSTANCE_SECURITY_GROUPS=basic_access
export CARO_CLOUD_INSTANCE_AVAILABILITY_ZONE=nova
export CARO_CLOUD_INSTANCE_NETWORK=private_network
export CARO_CLOUD_INSTANCE_IP=192.168.100.163

export CARO_CLOUD_SSH_USERNAME=centos
export CARO_CLOUD_SSH_KEYFILE=darknet-proto.pem

export CARO_DARKNET_FOLDER=$CARO_FOLDER/darknet
export CARO_DARKNET_LABEL=banana

export CARO_DARKNET_CFG=$CARO_DARKNET_FOLDER/yolov3-banana.cfg
export CARO_DARKNET_WEIGHTS=$CARO_DARKNET_FOLDER/yolov3-banana_16000.weights
export CARO_DARKNET_DATA=$CARO_DARKNET_FOLDER/banana.data
