# aws-k8-provisioner

Creates a K8 cluster using kOps on AWS. It uses ansbile script to automate the cluster creation and support some of the workflows that I generally run to execute my experiments. 

Steps were borrowed from:
https://aws.amazon.com/blogs/compute/kubernetes-clusters-aws-kops/

# Developer Guide

## Prerequisites

1. [Python3.12](https://www.python.org/downloads/)

## First Time Setup

This setup has been tested on MacOSX, Ubuntu and Fedora.

1. Create an environment using venv.
```bash
python3.12 -m venv aws
source aws/bin/activate
```

2. Install Python dependencies from the same directory as this README (remote_cluster).
```bash
python -m pip install -r requirements.txt
```

3. Install Ansible collections.
```bash
ansible-galaxy install -r requirements.yaml
```

4. Create `variables.yaml` and update the python interpreter.
```bash
cp -n playbooks/variables.yaml.example playbooks/variables.yaml
```

Inside `playbooks/variables.yaml`, update the value associated with the key `ansible_python_interpreter` to point to this environment (`which python`).
```yaml
ansible_python_interpreter: "<path to venv you created above>"
```

5. Create `secret.yaml` (copy `secret.yaml.example`) and update the values. The `s3name` should be the cluster status s3 store (currently `sre-bench` for the `us-east-2` cluster and `sre-bench-de` for the `eu-central-1` cluster) as well as your AWS credentials. If you do not need access to the cluster nodes, then you can leave the ssh key field blank. Otherwise, create an ssh key and provide the absolute path to the public key.
```bash
cp -n playbooks/secret.yaml.example playbooks/secret.yaml
```
```yaml
ssh_key_for_cluster: "/home/<user>/.ssh/<key-name>.pub"
```

6. To set up your local machine with the aws-cli, jq, kubectl and kops run. BECOME password is your user password or root password.
```bash
make configure_localmachine
```

7. Set up AWS credentials by running the following command. Enter the AWS access key ID and security access key when requested.
```bash
make configure_aws_access
```

## Cluster Management

1. Run the following command to create a cluster using EC2 resources. If you already have a cluster, you can skip this step. When prompted, supply the number of control nodes, worker nodes, name of the cluster, and type of instance required for the cluster. Recommended: 1 control node, 3 worker nodes, and instance type of m4.xlarge.
```bash
make create
```

2. Download kubeconf YAML file: it will list all clusters, type in one cluster name and it will download in `/tmp/`.  
   For example, if the cluster name appears as `exp-runner-m4.xlarge-aws-16.k8s.local\taws\tus-west-2a` you just need to enter everything up to and including .local `exp-runner-m4.xlarge-aws-16.k8s.local`.
```bash
make get_kcfg
```

3. Access remote k8s cluster
```bash
export KUBECONFIG=/tmp/<downloaded yaml>
kubectl get pod --all-namespaces
``` 

4. To destroy the cluster, run the following command:
```bash
make delete
```

## Expose services

1. Expose opentelemetry frontendproxy service: (`otel-demo` namespace is defined in [set_env_vars.sh](../set_env_vars.sh), `opentelemetry-demo-frontendproxy` is the service name from the output of `kubectl get svc -n otel-demo`.)
```bash
kubectl get svc -n otel-demo
kubectl port-forward svc/opentelemetry-demo-frontendproxy 8080:8080 -n otel-demo
```


## Makefile Options

For a full list of options, run the following command:
```bash
make help
```
