# Makefile to run Ansible playbooks

EXECUTE_CHECKS_IN_BACKGROUND ?= false
USE_JAEGER_QUERY_ENDPOINT ?= true

INCIDENT_NUMBER ?= 1

# TODO: Re-think the end to end experience

HOTEL_RESERVATION_SCENARIOS := 102 210 211 212

IS_DEBUG_SCENARIO ?= true
IS_HOTEL_RESERVATION_SCENARIO := $(shell echo "$(HOTEL_RESERVATION_SCENARIOS)" | grep -w "$(INCIDENT_NUMBER)" > /dev/null && echo "true" || echo "false")
SAMPLE_APPLICATION := $(shell echo "$(HOTEL_RESERVATION_SCENARIOS)" | grep -w "$(INCIDENT_NUMBER)" > /dev/null && echo "dsb_hotel_reservation" || echo "otel_astronomy_shop")

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-24s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: deploy_observability_stack
deploy_observability_stack: ## Deploys the observability tools to cluster
ifeq ($(USE_JAEGER_QUERY_ENDPOINT),false)
	ansible-playbook -v base.yaml --tags "install_tools" \
		--extra-vars "domain=sre" \
		--extra-vars "enable_jaeger_query_endpoint=false"
else
	ansible-playbook -v base.yaml --tags "install_tools" \
		--extra-vars "domain=sre" \
		--extra-vars "enable_jaeger_query_endpoint=true"
endif

.PHONY: undeploy_observability_stack
undeploy_observability_stack: ## Undeploys observability tools to cluster
	ansible-playbook -v base.yaml --tags "uninstall_tools" \
		--extra-vars "domain=sre"

.PHONY: deploy_finops_stack
deploy_finops_stack: ## Deploys the finops tools to cluster
	ansible-playbook -v base.yaml --tags "install_tools" \
		--extra-vars "domain=finops"

.PHONY: undeploy_finops_stack
undeploy_finops_stack: ## Undeploys finops tools to cluster
	ansible-playbook -v base.yaml --tags "uninstall_tools" \
		--extra-vars "domain=finops"

.PHONY: deploy_astronomy_shop
deploy_astronomy_shop: ## Deploys the Astronomy Shop application
	ansible-playbook -v base.yaml --tags "install_sample_applications" \
		--extra-vars "sample_application=otel_astronomy_shop"

.PHONY: undeploy_astronomy_shop
undeploy_astronomy_shop: ## Undeploys the Astronomy Shop application
	ansible-playbook -v base.yaml --tags "uninstall_sample_applications" \
		--extra-vars "sample_application=otel_astronomy_shop"

.PHONY: deploy_hotel_reservation
deploy_hotel_reservation: ## Deploys the Hotel Reservation application
	ansible-playbook -v base.yaml --tags "install_sample_applications" \
		--extra-vars "sample_application=dsb_hotel_reservation"

.PHONY: undeploy_hotel_reservation
undeploy_hotel_reservation: ## Undeploys the Hotel Reservation application
	ansible-playbook -v base.yaml --tags "uninstall_sample_applications" \
		--extra-vars "sample_application=dsb_hotel_reservation"

.PHONY: install_chaos_mesh
install_chaos_mesh: ## Installs a Chaos mesh to the cluster
	ansible-playbook -v base.yaml --tags "chaos_mesh_installation" \
		--extra-vars "is_install_chaos_mesh=true"

.PHONY: inject_incident_fault
inject_incident_fault: ## Injects the fault used in a specific incident
ifeq ($(IS_DEBUG_SCENARIO),true)
	ansible-playbook -v base.yaml --tags "incident_$(INCIDENT_NUMBER)" \
		--extra-vars "debug=true" \
		--extra-vars "is_fault_injection=true" \
		--extra-vars "incident_number=$(INCIDENT_NUMBER)" \
		--extra-vars "sample_application=$(SAMPLE_APPLICATION)"
else
	ansible-playbook -v base.yaml --tags "incident_$(INCIDENT_NUMBER)" \
		--extra-vars "is_fault_injection=true" \
		--extra-vars "incident_number=$(INCIDENT_NUMBER)" \
		--extra-vars "sample_application=$(SAMPLE_APPLICATION)"
endif

.PHONY: remove_incident_fault
remove_incident_fault: ## Removes the fault used in a specific incident
ifeq ($(IS_DEBUG_SCENARIO),true)
	ansible-playbook -v base.yaml --tags "incident_$(INCIDENT_NUMBER)" \
		--extra-vars "debug=true" \
		--extra-vars "is_fault_removal=true" \
		--extra-vars "incident_number=$(INCIDENT_NUMBER)" \
		--extra-vars "sample_application=$(SAMPLE_APPLICATION)"
else
	ansible-playbook -v base.yaml --tags "incident_$(INCIDENT_NUMBER)" \
		--extra-vars "is_fault_removal=true" \
		--extra-vars "incident_number=$(INCIDENT_NUMBER)" \
		--extra-vars "sample_application=$(SAMPLE_APPLICATION)"
endif

.PHONY: start_incident
ifeq ($(IS_HOTEL_RESERVATION_SCENARIO),true)
start_incident: deploy_observability_stack deploy_hotel_reservation inject_incident_fault ## Starts an incident by deploying a stack, application, and fault for an incident
else 
start_incident: deploy_observability_stack deploy_astronomy_shop inject_incident_fault
endif

.PHONY: stop_incident
ifeq ($(IS_HOTEL_RESERVATION_SCENARIO),true)
stop_incident: remove_incident_fault undeploy_hotel_reservation undeploy_astronomy_shop undeploy_observability_stack ## Stops an incident by undeploying a stack, application, and fault for an incident
else
stop_incident: remove_incident_fault undeploy_astronomy_shop undeploy_astronomy_shop undeploy_observability_stack
endif

.PHONY: awx_setup
awx_setup:
	ansible-playbook -v base.yaml --tags "awx_setup"

.PHONY: awx_configure_init
awx_configure_init:
	ansible-playbook -v base.yaml --tags "awx_configuration" --extra-vars "state=present"

.PHONY: awx_configure_deinit
awx_configure_deinit:
	ansible-playbook -v base.yaml --tags "awx_configuration" --extra-vars "state=absent"

# TODO: See why the OBJC_DISABLE_INITIALIZE_FORK_SAFETY is needed

.PHONY: documentation
documentation: ## Generates documentation for all incidents
	export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES; \
	ansible-playbook base.yaml --tags "documentation"

.PHONY: validate_docs
validate_docs: ## Validates documention for an incident
	export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES; \
	ansible-playbook base.yaml --tags "single_doc_validate,incident_$(INCIDENT_NUMBER)" \
		--extra-vars "doc_incident_number=$(INCIDENT_NUMBER)"

.PHONY: check_alerts
check_alerts:
ifeq ($(EXECUTE_CHECKS_IN_BACKGROUND),false)
	ansible-playbook -v base.yaml --tags "book_keeping" \
		--extra-vars "is_book_keeping=true" \
		--extra-vars "sample_application=$(SAMPLE_APPLICATION)" \
		$(BOOK_KEEPING_EXTRA_VARS)
else
	nohup ansible-playbook -v base.yaml --tags "book_keeping" \
		--extra-vars "is_book_keeping=true" \
		--extra-vars "sample_application=$(SAMPLE_APPLICATION)" \
		$(BOOK_KEEPING_EXTRA_VARS) &
endif
