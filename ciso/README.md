# CISO (Chief Information Security Officer) Sample Task Scenarios

Here is an example of Task Scenario used in an automation package to benchmark Agent for CISOs on [the IT-Bench](https://github.ibm.com/project-polaris/agent-bench-automation).

This repository contains following 4 category of scenarios:

```
.
├── 1.gen-cis-b-k8s-kyverno
├── 2.gen-cis-b-k8s-kubectl-opa
├── 3.gen-cis-b-rhel9-ansible-opa
├── 4.upd-cis-b-k8s-kyvernoz
└── README.md
```

Each scenario includes a setup for a compliance misconfigured environment and tools to check and address if the misconfiguration is resolved or not. 

For the detailed design, please refer to [IT-Bench Design Doc](https://github.ibm.com/project-polaris/agent-bench-automation/blob/main/docs/bench-design-doc.md).

## Scenarios

### 1. gen-cis-b-k8s-kyverno
**Description**: This scenario expects to deploy Kyverno policies to detect injected compliance issues in a Kubernetes environment for the compliance requirement "Minimize the admission of containers wishing to share the host network namespace".

#### 1.1 The agent is expected to do following task request (template value will be substituted):

```
I would like to check if the following condition is satisfiled, given a Kubernetes cluster with `kubeconfig.yaml`
Minimize the admission of containers wishing to share the host network namespace

To check the condition, do the following steps. 
- deploy a Kyverno policy to the cluster
- chcek if the policy is correctly deployed. 

If deploying the policy failed and if you can fix the issue, you will do it and try deploying again.
Once you get a final answer, you can quit the work.

The cluster's kubeconfig is at `{{ kubeconfig }}`.
```

When an agent is invoked, an input is provided about this scenario. The input is the json following schema. (You can get the exact value by `make get`)

```json
{
    "metadata": {
        "name": "cis-b.5.2.5-gen",  // Scenario Name
        "description": "CIS Benchmark for K8S 5.2.5 (Kyverno)", // Scenario Description
        "scenario_type": "Gen-CIS-b-K8s-Kyverno" // Scenario Type
    },
    // The above goal description
    "goal_template": "I would like to check if the following condition is satisfiled, given a Kubernetes cluster with `kubeconfig.yaml`\n    Minimize the admission of containers wishing to share the host network namespace.\n\nTo check the condition, do the following steps. \n- deploy a Kyverno policy to the cluster\n- chcek if the policy is correctly deployed. \n\nIf deploying the policy failed and if you can fix the issue, you will do it and try deploying again.\nOnce you get a final answer, you can quit the work.\n\nThe cluster's kubeconfig is at `{{ kubeconfig }}`.\n",
    "vars": {
        "kubeconfig": "apiVersion: v1\ncluster...="  // kubeconfig.yaml contents for access to the target Kubernetes
    }
}
```

#### 1.2 How it is evaluated

The evaluation verifies the following to return a pass:
- Verify that the specified Kyverno policy produces the expected Kyverno policy report for the target resource.

Please refer to [evaluation/main.py](/ciso/1.gen-cis-b-k8s-kyverno/evaluation/main.py) for the details.

#### The contents of the directory**:
```
├── 1.k8s-kyverno
│   ├── evaluation  # Tools or scripts to check if the injected security issues are detected or not in this scenario
│   ├── manifests   # Kubernetes resources to be deployed for compliance violation 
│   ├── playbooks   # Ansible playbooks to set up the scenario environment
│   ├── examples    # Example Kyverno Policy to detect the compliance violation
│   └── Makefile    # Commands to simplify setup and execution for the scenario
```

### 2. gen-cis-b-k8s-kubectl-opa
**Description**: This scenario expects to use kubectl to collect the Kubernetes resources and OPA (Open Policy Agent) to check if the injected compliance issues are detected or not for the compliance requirement "Minimize the admission of containers wishing to share the host network namespace".

#### 2.1 The agent is expected to do following task request (template value will be substituted):

```
I would like to check if the following condition is satisfiled, given a Kubernetes cluster with `kubeconfig.yaml`
    Minimize the admission of containers wishing to share the host network namespace

To check the condition, do the following steps. 
- get related resource(s) on the cluster by kubectl command
- chcek if the conditions are satisfied by OPA Rego policy

for those steps, you need to create an OPA Rego policy `policy.rego`. 
Also, save the kubectl command as `script.sh` with the following design. 
- The script should output the collected related resources to a file named `collected_data.json` in the current working directory.
- Please remove any kubeconfig configuration (e.g. --kubeconfig args) from the script, as users will configure the kubeconfig using environment variables or other methods.

If running the policy failed and if you can fix the issue, you will do it and try running again.

Once you get a final answer, you can quit the work.

The cluster's kubeconfig is at `{{ kubeconfig }}`.
```

When an agent is invoked, an input is provided about this scenario. The input is the json following schema. (You can get the exact value by `make get`)
```json
{
    "metadata": {
        "name": "k8s-opa/cis-b-gen/5.2.5", // Scenario Name
        "description": "CIS Benchmark for K8S 5.2.5 (OPA)", // Scenario Description
        "scenario_type": "Gen-CIS-b-K8s-Kubectl-OPA" // Scenario Type
    },
    // The above goal description
    "goal_template": "I would like to check if the following condition is satisfiled, given a Kubernetes cluster with `kubeconfig.yaml`\n    Minimize the admission of containers wishing to share the host network namespace. \n\nTo check the condition, do the following steps. \n- get related resource(s) on the cluster by kubectl command\n- chcek if the conditions are satisfied by OPA Rego policy\n\nfor those steps, you need to create an OPA Rego policy `policy.rego`. \nAlso, save the kubectl command as `script.sh` with the following design. \n- The script should output the collected related resources to a file named `collected_data.json` in the current working directory.\n- Please remove any kubeconfig configuration (e.g. --kubeconfig args) from the script, as users will configure the kubeconfig using environment variables or other methods.\n\nIf running the policy failed and if you can fix the issue, you will do it and try running again.\n\nOnce you get a final answer, you can quit the work.\n\nThe cluster's kubeconfig is at `{{ kubeconfig }}`.\n",
    "vars": {
        "kubeconfig": "apiVersion: v1\nclusters:\n- ..." // kubeconfig.yaml contents for access to the target Kubernetes
    }
}
```

#### 2.2 How it is evaluated

The evaluation verifies the following to return a pass:
- Confirm that the script.sh and policy.rego are produced.
- Ensure that script.sh runs successfuly and verify that the collected_data.json is produced.
- Ensure that OPA command runs successfully with the policy.rego against the collected_data.json. 
- Verify that the OPA outputs expected result.

Please refer to [evaluate.yml](/ciso/2.gen-cis-b-k8s-kubectl-opa/playbooks/evaluate.yml) for the details.

#### The contents of the directory
```
├── 2.k8s-kubectl-opa
│   ├── evaluation  # Tools or scripts to check if the injected security issues are detected or not in this scenario
│   ├── manifests   # Kubernetes resources to be deployed for compliance violation 
│   ├── playbooks   # Ansible playbooks to set up the scenario environment
│   ├── examples    # Example scripts to fetch Kubernetes resources and OPA Rego policy to check if the statuses complies or not 
│   └── Makefile    # Commands to simplify setup and execution for the scenario
```

### 3. gen-cis-b-rhel9-ansible-opa
**Description**: This scenario expects to use Ansible Playbooks to collect system status from RHEL9 and OPA to check if the injected compliance issues are detected or not for the compliance requirement "Ensure SSH X11 forwarding is disabled".

#### 3.1 The agent is expected to do following task request (template value will be substituted):

```
I would like to check if the following condition is satisfiled, given a host name `rhel9_servers`, on RHEL by using Ansible Playbook and OPA Rego policy
    Ensure SSH X11 forwarding is disabled

To check the condition, do the following steps. 
- collect configuration from the RHEL host and save it locally. you can use ansible-playbook to do that. 
- chcek if the condition is met by using rego policy with the input given by the step above. 

for those steps, you need to create ansible playbook `playbook.yml` and OPA rego policy `policy.rego`.
The playbook is implemented to locate the collected data to a file named `collected_data.json` in the current working directory.

If you can fix the generated code, do it and run the fixed code again.
Once you get a final answer, you can quit the work.

The Ansible inventory file (inventory.ansible.ini) for the target RHEL server is located at `{{ path_to_inventory }}`.
```

When an agent is invoked, an input is provided about this scenario. The input is the json following schema. (You can get the exact value by `make get`)
```json
{
"metadata": {
    "name": "rhel9/cis-b-gen/5.2.12", // Scenario Name
    "description": "CIS Benchmark for RHEL9 5.2.12", // Scenario Description
    "scenario_type": "Gen-CIS-b-RHEL9-Ansible-OPA" // Scenario Type
    },
    // The above goal description
    "goal_template": "I would like to check if the following condition is satisfiled, given a host name `rhel9_servers`, on RHEL by using Ansible Playbook and OPA Rego policy\n    Ensure SSH X11 forwarding is disabled \n\nTo check the condition, do the following steps. \n- collect configuration from the RHEL host and save it locally. you can use ansible-playbook to do that. \n- chcek if the condition is met by using rego policy with the input given by the step above. \n\nfor those steps, you need to create ansible playbook `playbook.yml` and OPA rego policy `policy.rego`.\nIf you can fix the generated code, do it and run the fixed code again.\nOnce you get a final answer, you can quit the work.\n\nThe Ansible inventory file (inventory.ansible.ini) for the target RHEL server is located at `{{ path_to_inventory }}`.\n",
    "vars": {
        "ansible_ini": "[rhel9_servers]\nrhel9 ansible_host=...", // Ansible Ini file to acceess to the target RHEL system
        "ansible_user_key": "***" // SSH Key
    }
}
```

#### 3.2 How it is evaluated

The evaluation verifies the following to return a pass:
- Confirm that the playbook.yml and policy.rego are produced.
- Ensure that playbook.yml runs successfuly and verify that the collected_data.json is produced.
- Ensure that OPA command runs successfully with the policy.rego against the collected_data.json. 
- Verify that the OPA outputs expected result.

Please refer to [evaluate.yml](/ciso/3.gen-cis-b-rhel9-ansible-opa/playbooks/evaluate.yml) for the details.

#### The contents of the directory
```
├── 3.rhel9-ansible-opa
│   ├── evaluation  # Tools or scripts to check if the injected security issues are detected or not in this scenario
│   ├── playbooks   # Ansible playbooks to set up the scenario environment
│   ├── examples    # Example Ansible Playbook to fetch system statuses and OPA Rego policy to check if the statuses complies or not 
│   └── Makefile    # Commands to simplify setup and execution for the scenario
│   └── tasks
│       ├── fault_inject.yml # Ansible task to make the RHEL system compliance violation
```

### 4. upd-cis-b-k8s-kyvernoz
**Description**: This scenario expects to inspect the current Kyvero policies and Kubernetes resources, then update the existing policies to comply the new compliance requirements.

#### 4.1 The agent is expected to do following task request (template value will be substituted):

```
Currently, the following Kyverno policies are deployed in the Kubernetes cluster. Review these existing policies and edit them to meet additional security requirements. Please avoid creating new policy resources; instead, make the necessary changes directly to the existing resources.

    Prohibit the use of the default service account
    Prohibit privilege escalation

However, the new internal security policy now requires the following additional conditions:

    Prohibit running as the root user
    Only allow signed images from a trusted registry (trusted-registry.com)

Your task is to review the existing Kyverno policies and directly edit the existing policies to meet these new requirements. Do not change the resource names. Once you have completed the edits, update the existing resources in the Kubernetes cluster.
Steps

    Review and Edit Kyverno Policies
    Directly modify the existing policy resources to meet the new requirements. Ensure that you do not change the names of the resources.

The cluster's kubeconfig is at `{{ kubeconfig }}`.
```

When an agent is invoked, an input is provided about this scenario. The input is the json following schema. (You can get the exact value by `make get`)
```json
{
    "metadata": {
        "name": "policy-adapt/scenario1", // Scenario Name
        "description": "Kyverno Policy Adapting: Enhancing Policies for Root and Trusted Registry Requirements", // Scenario Description
        "scenario_type": "Upd-CIS-b-K8s-Kyverno" // Scenario Type
    },
    // The above goal description
    "goal_template": "Currently, the following Kyverno policies are deployed in the Kubernetes cluster. Review these existing policies and edit them to meet additional security requirements. Please avoid creating new policy resources; instead, make the necessary changes directly to the existing resources.\n\n    Prohibit the use of the default service account\n    Prohibit privilege escalation\n\nHowever, the new internal security policy now requires the following additional conditions:\n\n    Prohibit running as the root user\n    Only allow signed images from a trusted registry (trusted-registry.com)\n\nYour task is to review the existing Kyverno policies and directly edit the existing policies to meet these new requirements. Do not change the resource names. Once you have completed the edits, update the existing resources in the Kubernetes cluster.\nSteps\n\n    Review and Edit Kyverno Policies\n    Directly modify the existing policy resources to meet the new requirements. Ensure that you do not change the names of the resources. \n\nThe cluster's kubeconfig is at `{{ kubeconfig }}`.\n",
    "vars": {
        "kubeconfig": "apiVersion: v1\nclusters..." // kubeconfig.yaml contents for access to the target Kubernetes
    }
}
```


#### 4.2 How it is evaluated

The evaluation verifies the following to return a pass:
- Verify that the specified Kyverno policy produces the expected Kyverno policy report for the target resource.
- Ensure that no modifications have been made to policies that should not be updated, and that no new policies have been created.

Please refer to [evaluation.py](/ciso/4.upd-cis-b-k8s-kyverno/evaluation.py) for the details.

#### The contents of the directory
```
├── 4.updating-k8s-kyverno
│   ├── evaluation  # Tools or scripts to check if the injected security issues are detected or not in this scenario
│   ├── manifests   # Kubernetes resources to be deployed for compliance violation 
│   ├── playbooks   # Ansible playbooks to set up the scenario environment
│   ├── examples    # Example Kyverno Policy to detect the compliance violation
│   └── Makefile    # Commands to simplify setup and execution for the scenario
```

## Try Sample CISO Scenarios with CISO Agent

Each scenario contains Makefile that contains the following targets. Benchmark Runner invokes these targets.

- deploy_bundle: setup the target environment
- inject_fault: deploy or configure the target environment so it violates the compliance requirement
- get: get the scenario details that would be passed as the input for Agent
- evaluate: valuate
- get_status: get status
- destroy_bundle: delete the target environment
- revert_bundle: revert the target environment

### ⚠ **Disclaimer: This process may modify or delete your environment**
Running the sample scenarios may modify or delete parts of your environment.  
- **Kubernetes-related scenarios**:  
  - `deploy_bundle` **creates a Kind cluster**, and `destroy_bundle` **deletes it**.  
- **RHEL-related scenarios**:  
  - Temporarily **adds and removes users** in the target RHEL environment.  
  - **Modifies system configurations** (e.g., `/etc/ssh/sshd_config`) for fault injection.  
- **General impact**:
  - Creates temporary files and directories under `/tmp` on the machine where the commands are executed.

💡 **Please run these commands only in a test environment or sandbox where any changes will not cause issues.**

### 1. Task Scenario for Targeting Kubernetes Cluster with Kyverno

The followings are for `1.gen-cis-b-k8s-kyverno` and `4.upd-cis-b-k8s-kyverno`

#### Pre-requisites (Tested on macOS. Compatibility with other platforms may vary.)
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

#### Steps
1. Go to the directory of a bundle (e.g. `cd 1.gen-cis-b-k8s-kyverno`.)
1. Create a scenario environment
    This command creates a Kind Cluster and install Kyverno to the cluster (the cluster name is "scenarios-ciso" as default. You can change it at "cluster_name" in /playbooks/vars.yaml.) It takes few minutes to finish.
    - `make deploy_bundle FOREGROUND=true`
    
        e.g.
        ```
        $ make deploy_bundle FOREGROUND=true
        ...
        TASK [Write updated status (with or without kubeconfig) back to JSON file] ***********************************************
        changed: [localhost]

        PLAY RECAP ***************************************************************************************************************
        localhost                  : ok=57   changed=10   unreachable=0    failed=0    skipped=11   rescued=0    ignored=0   
        ```
    - The kubconfig is available `/tmp/scenario-ciso-1/kubeconfig.caa.yaml`. The kubeconfig is available at /tmp/scenario-ciso-\<X\>/kubeconfig.caa.yaml, where \<X\> varies depending on the scenario (e.g., 1 for 1.gen-cis-b-k8s-kyverno, 2 for 2.gen-cis-b-k8s-kubectl-opa, etc.)
1. Inject compliance issues into the environment
    This command deploys nginx that violates the policy to minimize the admission of containers wishing to share the host network namespace. (hostNetwork is set to true)
    - `make inject_fault FOREGROUND=true`
    
        e.g.
        ```
        $ make inject_fault FOREGROUND=true
        PLAY [Execute fault injection] *******************************************************************************************
        ...
        PLAY RECAP ***************************************************************************************************************
        localhost                  : ok=29   changed=3    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0   
        ```
    - Now a pod that violates the policy to minimize the admission of containers wishing to share the host network namespace. (hostNetwork is set to true)
        ```
        $ export KUBECONFIG=/tmp/scenario-ciso-1/kubeconfig.caa.yaml
        $ kubectl get pod -n paa
        NAME                                READY   STATUS    RESTARTS   AGE
        nginx-deployment-7cb5b996ff-vb8mz   1/1     Running   0          1m
        ```
        ```
        $ kubectl get pod -n paa nginx-deployment-7cb5b996ff-vb8mz -o yaml
          apiVersion: v1
          kind: Pod
          metadata:
            creationTimestamp: "2025-01-17T06:26:41Z"
          spec:
            containers:
            - image: nginx:1.14.2
              imagePullPolicy: IfNotPresent
              ...
            hostNetwork: true
          ...
        ```
1. Get the goal and invoke your Agent to satisfy the goal
    ```
    $ make get 2>/dev/null
    {
      "metadata": {
        "name": "cis-b.5.2.5-gen",
        "description": "CIS Benchmark for K8S 5.2.5 (Kyverno)",
        "incident_type": "policy_gen",
        "scenario_type": "Gen-CIS-b-K8s-Kyverno",
        "goal": "Minimize the admission of containers wishing to share the host network namespace."
      },
      "goal_template": "I would like to check if the following condition is satisfiled, given a Kubernetes cluster with `kubeconfig.yaml`\n    Minimize the admission of containers wishing to share the host network namespace.\n\nTo check the condition, do the following steps. \n- deploy a Kyverno policy to the cluster\n- chcek if the policy is correctly deployed. \n\nIf deploying the policy failed and if you can fix the issue, you will do it and try deploying again.\nOnce you get a final answer, you can quit the work.\n\nThe cluster's kubeconfig is at `{{ kubeconfig }}`.\n",
      "vars": {
        "kubeconfig": "..."
      }
    }
    ```
1. Next, actually run CISO Agent to solve the given goal. To do that, please store the obtained `kubeconfig` from `make get` to a file and also replace the `{{ kubeconfig }}` in the `goal_template`. Note that this process is for the case of CISO Agent. It depends on agent how we prepare the input for an AI Agent. The following steps are example steps for the preparation of the CISO Agent. Please see [CISO Agent Getting started](https://github.ibm.com/project-polaris/ciso-agent) for the details.
    1. Save the kubeconfig
        - `mkdir -p /tmp/agent-workspace`
        - `make get 2>/dev/null | jq -r .vars.kubeconfig > /tmp/agent-workspace/kubeconfig.yaml`
    1. Replace the `{{ kubeconfig }}` with the saved file path in the `goal_template` when you run CISO Agent.
        - `make get 2>/dev/null | jq -r .goal_template | sed "s|{{ kubeconfig }}|/tmp/agent-workspace/kubeconfig.yaml|g" > /tmp/agent-workspace/goal.txt`
    1. Add a directive for working directory.
        - `echo "You can use '/tmp/agent-workspace' as your workdir." >> /tmp/agent-workspace/goal.txt`
1. Run the CISO agent (https://github.ibm.com/project-polaris/ciso-agent).
1. Once your agent is finished, run evaluation.
    - `make evaluate`

        e.g.
        ```
        $ make evaluate
        ansible-playbook ./playbooks/evaluate.yml --extra-vars "path_to_output=/tmp/scenario-ciso-1/evaluation.json " &> /tmp/scenario-ciso-1/evaluate.log
            {
            "pass": true,
            "tasks": {
                "generate_assessment_posture": true,
                "generate_policy": false,
                "evidence_available": false
            }
        }       
        ```
    - If the `pass` is `true`, the CISO Agent has successfully deployed the correct Kyverno Policy. You can check the Kyverno Policy that the CISO Agent created.
        ```
        $ kubectl get clusterpolicy
        NAME                          ADMISSION   BACKGROUND   READY   AGE     MESSAGE
        deny-host-network-namespace   true        true         True    5m39s   Ready
        ```
    - Also, you can check that Kyverno reports the policy alert based againt the injected fault deployment on this policy.
        ```
        $ kubectl get policyreport -n paa
        NAME                                   KIND         NAME                                PASS   FAIL   WARN   ERROR   SKIP   AGE
        2f6bbe6e-4f1c-4381-b5c8-b1ff4adb7121   ReplicaSet   nginx-deployment-7cb5b996ff         0      1      0      0       0      6m45s
        335b8723-9c40-41ce-acc1-5cad0f5bdfb7   Deployment   nginx-deployment                    0      1      0      0       0      6m45s
        4868fc81-2b55-4981-9bc7-def313f74619   Pod          nginx-deployment-7cb5b996ff-vb8mz   0      1      0      0       0      6m45s
        ```
1. Now you successfully finished a single evaluation of the Agent. You can cleanup (delete cluster) or if you want to try again, run `make revert`, which removes fault injections, kyverno resources (policy and policy reports).
    - `make destroy_bundle FOREGROUND=true` or `make revert FOREGROUND=true`

### 2. Task Scenario for Targeting Kubernetes Cluster with Kubectl+OPA

The followings are for `2.gen-cis-b-k8s-kubectl-opa`

#### Pre-requisites
Same as [Task Scenario for Targeting Kubernetes Cluster with Kyverno](#task-scenario-for-targeting-kubernetes-cluster-with-kyverno)

#### Steps
Same as Steps 1-6, as described in [Task Scenario for Targeting Kubernetes Cluster with Kyverno](#task-scenario-for-targeting-kubernetes-cluster-with-kyverno)

The only different step is evaluation. For this step, you need to place the agent output in the directory used for evaluation, as this scenario expects the Agent to generate a script for data collection and an OPA Rego policy for compliance-checking the collected data.

1. Once the Agent has finished, ensure that the Agent output includes playbool.yml and policy.rego.
    For example, if the Agent outputs the playbook and policy in `/tmp/agent-workspace`
1. Run evaluation
    - `make evaluate SHARED_WORKSPACE=/tmp/agent-workspace`

        e.g.
        ```
        make evaluate SHARED_WORKSPACE=/tmp/agent-workspac

        {"pass": true, "details": "[fetcher] cmd: ['bash', '/tmp/agent-workspace/fetcher.sh'], stdout: , stderr: \n[checker] cmd: ['opa', 'eval', '--data', '/tmp/agent-workspace/policy.rego', '--input', '/tmp/agent-workspace/collected_data.json', 'data.check.result', '--format', 'raw'], stdout: false, stderr: \n"}
        ```
    - If the `pass` is `true`, the CISO Agent has successfully created a script for resource collection from Kubernetes and OPA policy for compliance checking aganst the collected data.
1. Now you successfully finished a single evaluation of the Agent. You can cleanup (delete cluster) or if you want to try again, run `make revert`, which only removes Kubernetes resources deployed at fault injection.
    - `make destroy_bundle FOREGROUND=true` or `make revert FOREGROUND=true`

### 3. Task Scenario for Targeting Red Hat Enterprise Linux 9

#### Pre-requisites (Tested on macOS. Compatibility with other platforms may vary.)
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
1. Red Hat Enterprise Linux 9 with admininistrative access (at least the task scenario needs permission to create a temporal user)

#### Steps
1. Create input.json
    Fill in the `target_server.address`, `target_server.username`, and `target_server.sshkey` fields in the `input.json` located in the `3.gen-cis-b-rhel9-ansible-opa` directory.
1. Create a scenario environment
    This command creates a temporary user on the target RHEL machine. The default username is `ansible_user`. You can modify the name in the `check_target_user` variable in `playbooks/vars.yaml`.
    - `make deploy_bundle INPUT_FILE=./input.json FOREGROUND=true`
    
        e.g.
        ```
        $ make deploy_bundle INPUT_FILE=./input.json FOREGROUND=true
        ...
        TASK [Write updated status back to JSON file] ****************************************************************************
        changed: [RHEL9 Machine -> localhost]

        PLAY RECAP ***************************************************************************************************************
        RHEL9 Machine              : ok=32   changed=10   unreachable=0    failed=0    skipped=2    rescued=0    ignored=0   
        ```
    - The temporary user's credentials and the inventory ini file for running Ansible with the user are located in /tmp/scenario-ciso-3 directory.
        ```
        $ ls /tmp/scenario-ciso-3
        id_rsa.ansible_user   input.json            inventory.ansible.ini status.json
        ```
1. Inject compliance issues into the environment
    This command applies non-compliant settings to the system to simulate compliance issues. Please see [3.gen-cis-b-rhel9-ansible-opa/tasks/fault_inject.yml](/ciso/3.gen-cis-b-rhel9-ansible-opa/tasks/fault_inject.yml) for what is injected.
    - `make inject_fault INPUT_FILE=./input.json FOREGROUND=true`
    
        e.g.
        ```
        $ make inject_fault INPUT_FILE=./input.json FOREGROUND=true
        PLAY [Execute fault injection] *******************************************************************************************
        ...
        PLAY RECAP ***************************************************************************************************************
        RHEL9 Machine              : ok=24   changed=4    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0   
        ```
1. Get the goal and invoke your Agent to satisfy the goal
    ```
    $ make get INPUT_FILE=./input.json 2>/dev/null
    {
    "metadata": {
        "name": "rhel9/cis-b-gen/5.2.12",
        "description": "CIS Benchmark for RHEL9 5.2.12",
        "incident_type": "rhel9-cis-b-gen",
        "scenario_type": "Gen-CIS-b-RHEL9-Ansible-OPA",
        "goal": "Ensure SSH X11 forwarding is disabled"
    },
    "goal_template": "I would like to check if the following condition is satisfiled, given a host name `rhel9_servers`, on RHEL by using Ansible Playbook and OPA Rego policy\n    Ensure SSH X11 forwarding is disabled \n\nTo check the condition, do the following steps. \n- collect configuration from the RHEL host and save it locally. you can use ansible-playbook to do that. \n- chcek if the condition is met by using rego policy with the input given by the step above. \n\nfor those steps, you need to create ansible playbook `playbook.yml` and OPA rego policy `policy.rego`.\nIf you can fix the generated code, do it and run the fixed code again.\nOnce you get a final answer, you can quit the work.\n\nThe Ansible inventory file (inventory.ansible.ini) for the target RHEL server is located at `{{ path_to_inventory }}`.\n",
    "vars": {
        "ansible_ini": "[rhel9_servers]\nrhel9 ansible_host=\"ciso-server1.sl.cloud9.ibm.com\" ansible_user=\"ansible_user\" ansible_ssh_private_key_file=\"/tmp/scenario-ciso-3/id_rsa.ansible_user\" ansible_python_interpreter=\"/usr/bin/python3\"",
        "ansible_user_key": "-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn\nNhAAAAAwEA
        ...}
    }
    ```
1. Next, actually run CISO Agent to solve the given goal. To do that:
    1. Retrieve the ansible.ini file and the ansible_user_key.
        - `mkdir -p /tmp/agent-workspace`
        - `make get INPUT_FILE=./input.json 2>/dev/null | jq -r .vars.ansible_ini > /tmp/agent-workspace/ansible.ini`
1. Run the CISO agent (https://github.ibm.com/project-polaris/ciso-agent) by providing goal description obtained from `make get` with replaced `{{ path_to_inventory }}` with the ansible.ini (e.g. `/tmp/agent-workspace/ansible.ini`). 
1. Once the Agent has finished, ensure that the Agent output includes playbool.yml and policy.rego.
    For example, if the Agent outputs the playbook and policy in `/tmp/agent-workspace`
1. Run evaluation
    - `make evaluate INPUT_FILE=./input.json SHARED_WORKSPACE=/tmp/agent-workspace`

        e.g.
        ```
        make evaluate INPUT_FILE=./input.json SHARED_WORKSPACE=/tmp/agent-workspac
        {"pass": true, "details": "[fetcher] cmd: ['ansible-playbook', '/tmp/agent-workspace/playbook.yml', '-i', '/tmp/scenario-ciso-3/inventory.ansible.ini'], stdout: \nPLAY [Collect SSH configuration from RHEL host] ********************************\n\nTASK [Gathering Facts] *********************************************************\nok: [rhel9]\n\nTASK [Check if SSH X11 forwarding is disabled] *********************************\nchanged: [rhel9]\n\nTASK [Save SSH X11 forwarding configuration to a variable] *********************\nok: [rhel9]\n\nTASK [Save the collected data in a localhost] **********************************\nok: [rhel9 -> localhost]\n\nPLAY RECAP *********************************************************************\nrhel9                      : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   , stderr: \n[checker] cmd: ['opa', 'eval', '--data', '/tmp/agent-workspace/policy.rego', '--input', '/tmp/agent-workspace/collected_data.json', 'data.check.result', '--format', 'raw'], stdout: false, stderr: \n"}
        ```
    - If the `pass` is `true`, the CISO Agent has successfully created playbook for status collection and OPA policy for compliance checking aganst the collected data.
1. Now you successfully run a single evaluation of the Agent. You can revert the injected fault configuration and remove the temporal users
    - `make destroy_bundle INPUT_FILE=./my.input.json FOREGROUND=true`


## Try Benchmark
1. Start Benchmark Server
1. Start Benchmark Runner
1. Create sample-task-scenarios/ciso/scenario-bundles.json
    ```
    token=`curl -k -s -X POST \
        -H "Content-Type: application/x-www-form-urlencoded" \
        "https://localhost:8000/test/token" \
        -d "username=service_compliance&password=" | jq -r .access_token`
    curl -k -X POST \
        -H "Authorization: Bearer $token" \
        -H "Content-type: application/json" \
        "https://localhost:8000/test/registry/setup-scenarios" -d @sample-task-scenarios/ciso/scenario-bundles.json | jq
    ```
1. Go to Benchmark UI and create agent with Expert level and all categories selected
    ![registration](/ciso/images/registration.png)

1. Run Benchmark and finally obtain these 4 scenarios' scores
    ![registration](/ciso/images/leaderboard.png)
