"""
Module supporting the Cloud and the Ssh classes, responsible for creating a
cloud instance and for executing remote commands to it.

class Cloud: creates, manages and deletes cloud instances.

class Ssh: remotely access and run arbitrary commands on an instance.

initialize_connection : initialize a SSH connection configuration items.
"""

#pylint: disable=import-error

import time
import logging

import openstack
import paramiko.client as pc
import paramiko.ssh_exception as pe


class Cloud():
    """Creates and manages cloud instances.

    The class Cloud is limited to instance creation and deletion for one
    particular cloud setting, usually described in a configuration file,
    typically 'clouds.yaml'.

    Attributes:
        conn = A connection instance representing the connection to the cloud.
        instance = A tuple: (name, image, flavor)
        nets = A tuple: (security_groups, network, ips)
        volume = A tuple: (boot_volume, volume_size)
    """

    def __init__(self, cloud, instance, nets, volume):
        """Initialize a cloud class"""

        self._conn = openstack.connect(cloud=cloud)
        self._instance = instance
        self._nets = nets
        self._volume = volume


    @property
    def conn(self):
        """Getter for Cloud instance conn.

        Args:
            None

        Returns:
            A connection instance representing the cloud connection.
        """

        return self._conn


    @conn.setter
    def conn(self, cloud):
        """Setter for Cloud instance image.

        Args:
            image: A string representing the name of the image to use.

        Returns:
            None
        """

        self._conn = openstack.connect(cloud=cloud)


    @property
    def instance(self):
        """Getter for Cloud instance instance.

        Args:
            None

        Returns:
            A tuple representing the cloud instance.
        """

        return self._instance


    @instance.setter
    def instance(self, instance):
        """Setter for Cloud instance instance.

        Args:
            instance: A tuple representing the instance {name, image, flavor}.

        Returns:
            None
        """

        self._instance = instance


    @property
    def nets(self):
        """Getter for Cloud instance nets.

        Args:
            None

        Returns:
            A string representing the cloud nets.
        """

        return self._nets


    @nets.setter
    def nets(self, nets):
        """Setter for Cloud instance nets.

        Args:
            nets: A tuple representing nets {security_groups, network, ips}.

        Returns:
            None
        """

        self._nets = nets


    @property
    def volume(self):
        """Getter for Cloud instance volume.

        Args:
            None

        Returns:
            A string representing the cloud volume.
        """

        return self._volume


    @volume.setter
    def volume(self, volume):
        """Setter for Cloud instance volume.

        Args:
            volume: A tuple representing the volume {boot_volume, volume_size}.

        Returns:
            None
        """

        self._volume = volume


    def create_instance(self):
        """Creates a cloud instance.

        Args:
            None

        Returns:
            None
        """

        logging.info("creating instance %s", str(self.instance['name']))

        self.conn.create_server(self.instance['name'],
                                image=None,
                                flavor=self.instance['flavor'],
                                boot_volume=self.volume['boot_volume'],
                                boot_from_volume=True,
                                volume_size=self.volume['volume_size'],
                                terminate_volume=True,
                                security_groups=self.nets['security_groups'],
                                availability_zone="nova",
                                network=self.nets['network'],
                                ips=self.nets['ips'],
                                wait=True,
                                timeout=180)


    def delete_instance(self):
        """Deletes a cloud instance.

        Args:
            None

        Returns:
            None
        """

        logging.info("deleting instance %s", str(self.instance['name']))

        self.conn.delete_server(self.instance['name'])


def initialize_connection():
    """Initialize a SSH connection configuration items.

    Args:
        None

    Returns:
        A client instance used for initiating remote connections.
    """

    client = pc.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(pc.AutoAddPolicy())

    return client


class Ssh():
    """Class responsible for initiating connection and executing commands on a
    remote instance.

    Attributes:
        remote_ip = A string representing the remote IP to connect to.
        username = A string representing the username to employ for connection.
        key_filename = A string representing the path of the keyfile.
    """


    def __init__(self, remote_ip, username, key_filename):
        """Default builder for the Ssh class."""

        self._client = initialize_connection()
        self._remote_ip = remote_ip
        self._username = username
        self._key_filename = key_filename


    @property
    def client(self):
        """Getter for Ssh instance client.

        Args:
            None

        Returns:
            A client instance representing the client.
        """

        return self._client


    @client.setter
    def client(self):
        """Setter for Ssh client.

        Args:
            None

        Returns:
            None
        """

        self._client = initialize_connection()


    @property
    def remote_ip(self):
        """Getter for Ssh instance remote_ip.

        Args:
            None

        Returns:
            A string representing the remote_ip.
        """

        return self._remote_ip


    @remote_ip.setter
    def remote_ip(self, remote_ip):
        """Setter for Ssh remote_ip.

        Args:
            remote_ip: A string representing the remote_ip.

        Returns:
            None
        """

        self._remote_ip = remote_ip


    @property
    def username(self):
        """Getter for Ssh instance username.

        Args:
            None

        Returns:
            A string representing the username.
        """

        return self._username


    @username.setter
    def username(self, username):
        """Setter for Ssh username.

        Args:
            username: A string representing the username.

        Returns:
            None
        """

        self._username = username


    @property
    def key_filename(self):
        """Getter for Ssh instance key_filename.

        Args:
            None

        Returns:
            A string representing the key_filename path.
        """

        return self._key_filename


    @key_filename.setter
    def key_filename(self, key_filename):
        """Setter for Ssh key_filename.

        Args:
            key_filename: A string representing the key_filename path.

        Returns:
            None
        """

        self._key_filename = key_filename


    def remote_connect(self, retry_count):
        """Start a connection to a remote server.

        Args:
            retry_count: An int representing the number of connection attempts.

        Returns:
            None
        """

        logging.info("connecting to %s", self.remote_ip)

        count = 0

        while count < int(retry_count):
            try:

                self.client.connect(hostname=self.remote_ip,
                                    username=self.username,
                                    key_filename=self.key_filename)

                logging.info("connection to %s successful", self.remote_ip)

                break

            except pe.NoValidConnectionsError:
                logging.warning("connection to %s failed with %s attempts",
                                self.remote_ip, str(count))
                time.sleep(5)
                count += 1

        if count >= int(retry_count):
            logging.error("connection to %s timeout", self.remote_ip)


    def exec_command(self, command):
        """Executes a command remotely.

        Args:
            command: A string representing the command to execute.

        Returns:
           A tuple including the remote (STDIN, STDOUT, STDERR).
        """

        logging.info("executing command %s", str(command))

        stdin, stdout, stderr = self.client.exec_command(command)

        return (stdin, stdout, stderr)
