
# Pre-requisites
1. Miniconda / Anaconda (or venv)
2. [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

# Setup

## Local Cluster
This setup has been tested on MacOS.

Helm version v.3.16 is required: [Installation](https://helm.sh/docs/intro/install/).

#### Create an islated environment 
##### e.g., Python's virtual environments

```bash
#we use python 3.11
python3 -m venv venv
source venv/bin/activate
```


#### Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

#### Install podman
Tested on Podman Desktop. [Installation Instructions can be found here](https://podman.io/docs/installation)

And verify the installation:
```shell
podman info
```

#### Install kind
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

# Troubleshooting

**1. Running Kind cluster on Red Hat Enterprise Linux (RHEL) 9.5 with podman:**

Check the official "Red Hat Documentation" for information about installing podman.
During our test, we found that running kind with rootless provider on RHEL with podman will require some special setup which cannot be coverd here.
We used **sudo** previlege to create Kind cluster and ran the test successfully.
Please see [instructions](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) for the installation and setup kubectl on Linux if you don't have one installed.

`$ sudo kind create cluster --config local_cluster/kind-config.yaml`

Once the kind cluster is up and running, please run the following commands before using kubectl:
```
$ sudo cp /root/.kube/config /tmp
$ sudo chmod 644 /tmp/config
$ export KUBECONFIG=/tmp/config
```
```
$ kubectl get nodes
NAME                         STATUS   ROLES           AGE    VERSION
kind-cluster-control-plane   Ready    control-plane   7d1h   v1.30.0
```
**2. "CrashLoopBackOff" in Chaos-Controller Manager Pods on Red Hat Enterprise Linux (RHEL) 9.5**

**Problem:**  While testing on RHEL OS, the `chaos-controller-manager` pods in kind cluster may enter a `CrashLoopBackOff` state due to the error:  
```
"too many files open"
```

This is related to inotify resource limits, which can be exhausted in kind clusters, especially when there are many files being watched. This can impact the RHEL-based deployment of chaos mesh related scenarios. 

**Solution:** 
Fix for this problem is given in [KinD Known Issues - Pod Errors Due to Too Many Open Files](https://kind.sigs.k8s.io/docs/user/known-issues/#pod-errors-due-to-too-many-open-files). 

**Note:**
This issue has been observed specifically on RHEL OS while working within the chaos-mesh namespace. No such issue has been observed during testing on macOS.
