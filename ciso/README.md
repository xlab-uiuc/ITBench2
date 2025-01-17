# CISO (Chief Information Security Officer) Sample Task Scenarios

This repository provides sample task scenarios of the IT Benchmark for CISO. Each scenario includes a setup for a compliance misconfigured environment and tools to check and address if the misconfiguration is resolved or not.

This repository contains following 4 category of scenarios:

```
.
├── 1.gen-cis-b-k8s-kyverno
├── 2.gen-cis-b-k8s-kubectl-opa
├── 3.gen-cis-b-rhel9-ansible-opa
├── 4.upd-cis-b-k8s-kyvernoz
└── README.md
```

## Scenarios

### 1. gen-cis-b-k8s-kyverno
**Description**: This scenario expects to use Kyverno policies to detect injected compliance issues in a Kubernetes environment.

```
├── 1.k8s-kyverno
│   ├── evaluation  # Tools or scripts to check if the injected security issues are detected or not in this scenario
│   ├── manifests   # Kubernetes resources to be deployed for compliance violation 
│   ├── playbooks   # Ansible playbooks to set up the scenario environment
│   ├── examples    # Example Kyverno Policy to detect the compliance violation
│   └── Makefile    # Commands to simplify setup and execution for the scenario
```
### 2. gen-cis-b-k8s-kubectl-opa
**Description**: This scenario expects to use kubectl to collect the Kubernetes resources and OPA (Open Policy Agent) to check if the injected compliance issues are detected or not in this scenario.

```
├── 2.k8s-kubectl-opa
│   ├── evaluation  # Tools or scripts to check if the injected security issues are detected or not in this scenario
│   ├── manifests   # Kubernetes resources to be deployed for compliance violation 
│   ├── playbooks   # Ansible playbooks to set up the scenario environment
│   ├── examples    # Example scripts to fetch Kubernetes resources and OPA Rego policy to check if the statuses complies or not 
│   └── Makefile    # Commands to simplify setup and execution for the scenario
```
### 3. gen-cis-b-rhel9-ansible-opa
**Description**: This scenario expects to use Ansible Playbooks to collect system status from RHEL9 and OPA to check if the injected compliance issues are detected or not in this scenario.

```
├── 3.rhel9-ansible-opa
│   ├── evaluation  # Tools or scripts to check if the injected security issues are detected or not in this scenario
│   ├── playbooks   # Ansible playbooks to set up the scenario environment
│   ├── examples    # Example Ansible Playbook to fetch system statuses and OPA Rego policy to check if the statuses complies or not 
│   └── Makefile    # Commands to simplify setup and execution for the scenario
```

### 4. upd-cis-b-k8s-kyvernoz
**Description**: This scenario expects to inspect the current Kyvero policies, and update it to comply the new compliance requirements.

```
├── 4.updating-k8s-kyverno
│   ├── evaluation  # Tools or scripts to check if the injected security issues are detected or not in this scenario
│   ├── manifests   # Kubernetes resources to be deployed for compliance violation 
│   ├── playbooks   # Ansible playbooks to set up the scenario environment
│   ├── examples    # Example Kyverno Policy to detect the compliance violation
│   └── Makefile    # Commands to simplify setup and execution for the scenario
```

## Usage

### Pre-requisites (verified only on M1 Mac OSX)
1. Docker runtime (e.g. [Rancher Desktop](https://docs.rancherdesktop.io/getting-started/installation))
1. KinD (tested with 0.19.0)
    - For Rancher Desktop use, some older versions don't work with KinD. We have only tested on Rancher 1.16.0.
1. Kubectl (tested with v1.31.0)
1. Helm (tested with v3.16.1)
    - `brew install helm`
1. [OPA](https://www.openpolicyagent.org/) (tested with v1.0.0)
1. Ansible Playbook (tested with 2.17.4) and kubernetes.core module
    - From Homebrew
        - `brew install ansible`
    - From PyPI
        - `pip install ansible` (see also https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#pipx-install)
        - `ansible-galaxy collection install kubernetes.core`
        - `pip install jmespath kubernetes`
1. jq command
    - `brew install jq`

### Run Task Scenario
1. Go to the directory of a bundle (e.g. `cd cis-b.5.2.5-gen`)
1. Install a Bundle
    - `make deploy_bundle`
1. Inject compliance violation
    - `make inject_fault`
1. Now you can see compliance violation in `caa` namespace in Policy Report. 
    ```
    $ KUBECONFIG=/tmp/pac-bundle/cis-b.5.2.7-gen/kubeconfig.caa.yaml kubectl get polr -n paa
    NAME                                   KIND         NAME                                                PASS   FAIL   WARN   ERROR   SKIP   AGE
    0640a191-22f9-41fa-89b7-a7037184aef4   ReplicaSet   nginx-deployment-running-as-root-7dddd57785         0      1      0      0       0      27s
    16038981-6245-44a1-b96f-04ee6b6f5546   Deployment   nginx-deployment-running-as-root                    0      1      0      0       0      47s
    90864f01-f2c8-4004-a1e7-d0c7b08cb976   Pod          nginx-deployment-running-as-root-7dddd57785-gpvjc   0      1      0      0       0      47s
    ```
1. Get all (status, pass/fail, kubeconfig, and policy reports) 
    ```
    $ make get
    {
    "status": {
        "conditions": [
        {
            "type": "Deployed",
            "status": "True",
            "lastTransitionTime": "2024-10-04T23:54:52Z"
        }...],
    },
    "kubeconfig"
    "pass": false,
    "report": [...]
    ```
1. (Optional) Revert
    - `make revert`
1. Cleanup
    - `make destroy_bundle`

```
$ make help
Makefile commands:
deploy_bundle -- [onetime] deploys the bundle to the cluster
inject_fault -- [onetime] define a new policy (policies) and enable fault for hitting CIS Benchmark controls
destroy_bundle -- [onetime] destroy the target environment
revert_bundle -- [onetime] revert the target environment
get -- [onetime] get status and evaluation
get_status -- [onetime] get status
evaluate -- [onetime] evaluate
Option FOREGROUND=true for synchronous execution. Default execute as background job.
help   - Display this help information
```