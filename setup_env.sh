export CARO_LOGFILE=caro.log
export CARO_CAPTURE_FOLDER=$(pwd)/client/capture/
export CARO_INBOX_FOLDER=$(pwd)/server/inbox/
export CARO_FOLDER=$(pwd)/

export CARO_CLOUD_CONFIG_FILE=clouds.yaml

export CARO_CLOUD_NAME=eams_cloud
export CARO_CLOUD_INSTANCE_NAME=darknet-instance
export CARO_CLOUD_INSTANCE_IMAGE=None
export CARO_CLOUD_INSTANCE_FLAVOR=m1.compute
export CARO_CLOUD_INSTANCE_BOOT_VOLUME=d316e1b4-7109-4625-88b4-ef5f8ca20533
export CARO_CLOUD_INSTANCE_BOOT_VOLUME_SIZE=10
export CARO_CLOUD_INSTANCE_SECURITY_GROUPS=basic_access
export CARO_CLOUD_INSTANCE_AVAILABILITY_ZONE=nova
export CARO_CLOUD_INSTANCE_NETWORK=private_network
export CARO_CLOUD_INSTANCE_IP=192.168.100.163

export CARO_CLOUD_SSH_USERNAME=centos
export CARO_CLOUD_SSH_KEYFILE=darknet-proto.pem

export CARO_DARKNET_FOLDER=$(pwd)/darknet/
export CARO_DARKNET_LABEL=banana

export CARO_DARKNET_CFG=yolov3-banana.cfg
export CARO_DARKNET_WEIGHTS=yolov3-banana_16000.weights
export CARO_DARKNET_DATA=banana.data
