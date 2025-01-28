#!/bin/bash

# Common
export CLUSTER_NAME=""
export CLUSTER_KUBERNETES_OPENSHIFT_API_ENDPOINT=""

## Observability Tools
# Loki Configuration
export LOKI_NAMESPACE_PROJECT_NAME="loki"
export LOKI_INSTALLATION_NAME="loki-stack"

# OpenSearch Configuration
export OPENSEARCH_NAMESPACE_PROJECT_NAME="opensearch"
export OPENSEARCH_INSTALLATION_NAME="opensearch"
export OPENSEARCH_VERSION_NUMBER="2.17.1"

# Elasticsearch Configuration
export ES_NAMESPACE_PROJECT_NAME="elastic"
export ES_INSTALLATION_NAME="elastic"

# Prometheus - Grafana Configuration
export PROMETHEUS_NAMESPACE_PROJECT_NAME="prometheus"
export PROMETHEUS_INSTALLATION_NAME="prometheus-stack"

# Jaeger Configuration
export JAEGER_NAMESPACE_PROJECT_NAME="jaeger"
export JAEGER_INSTALLATION_NAME="jaeger"

# Event Exporter
export EVENT_EXPORTER_INSTALLATION_NAME="event-exporter"

## Sample Applications
# SimpleApp Configuration
export SIMPLE_APP_NAMESPACE_PROJECT_NAME="simple-us"

# RobotShop Configuration
export ROBOTSHOP_APP_NAMESPACE_PROJECT_NAME="robot-shop"
export ROBOTSHOP_APP_INSTALLATION_NAME="robot-shop"

# OTEL Astronomy Demo Configuration
export OTEL_ASTRONOMY_APP_NAMESPACE_PROJECT_NAME="otel-demo"
export OTEL_ASTRONOMY_APP_INSTALLATION_NAME="astronomy-demo"
