
# Pre-requisites
1. Miniconda / Anaconda (or venv)
2. [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

# Setup

## Local Cluster
This setup has been tested on Fedora.

### Install kind
```shell
# Based on https://kind.sigs.k8s.io/docs/user/quick-start#installing-from-release-binaries
# For AMD64 / x86_64
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
chmod +x ./kind
mv ./kind ~/bin/
```

And verify the installation:
```shell
$ which kind
/usr/local/bin/kind
$ kind version
kind v0.23.0 go1.21.10 linux/amd64
```

A barebone kind configuration file has been provided [here](./kind-config.yaml).

Let's create a kind cluster using the configuration file by executing:
```shell
$ kind create cluster --config local_cluster/kind-config.yaml
Creating cluster "kind-cluster" ...
 ✓ Ensuring node image (kindest/node:v1.30.0) 🖼
 ✓ Preparing nodes 📦
 ✓ Writing configuration 📜
 ✓ Starting control-plane 🕹️
 ✓ Installing CNI 🔌
 ✓ Installing StorageClass 💾
Set kubectl context to "kind-cluster"
You can now use your cluster with:

kubectl cluster-info --context kind-cluster

Have a question, bug, or feature request? Let us know! https://kind.sigs.k8s.io/#community 🙂
```

Let's verify the status of the clusters with:
```shell
$ kubectl cluster-info --context kind-cluster

Kubernetes control plane is running at https://127.0.0.1:36111
CoreDNS is running at https://127.0.0.1:36111/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```
```shell
$ kubectl get nodes
NAME                           STATUS   ROLES           AGE     VERSION\
kind-cluster-control-plane   Ready    control-plane   8m22s   v1.30.0
```
