from typing import List, Optional

from pydantic import (BaseModel, Field, StrictInt, ValidationInfo,
                      field_validator)


class AWXConfigurationModel(BaseModel):
    endpoint: str
    username: str = Field(default="admin")
    password: str


class GitConfigurationModel(BaseModel):
    it_automation_bench_local_path: str
    deploy_key_it_automation_bench_private_ssh_key_path: str
    deploy_key_agent_private_ssh_key_path: str
    deploy_key_agent_analytics_sdk_private_ssh_key_path: Optional[str] = None
    deploy_key_agent_analytics_sdk_ssh_key_passphrase: Optional[str] = None


class LLMConfigModel(BaseModel):
    llm_configuration_parameters: str
    llm_model_name: str
    llm_backend: str
    llm_base_url: str
    llm_api_key: str
    llm_project_id: Optional[str] = None


class AgentAnalyticsSDKModel(BaseModel):
    git_token: str
    git_username: str


class AgentConfigurationModel(BaseModel):
    llm_for_agents_config: LLMConfigModel
    llm_for_tools_config: LLMConfigModel
    enable_tools: Optional[List[str]] = None
    enable_god_mode: bool = Field(default=True)
    enable_tool_with_reflection: bool = Field(default=True)
    agent_analytics_sdk: AgentAnalyticsSDKModel

    @field_validator('llm_for_agents_config', mode='after')
    @classmethod
    def is_llm_for_agents_config__equals__llm_for_tools_config(
            cls, value: str, info: ValidationInfo) -> str:
        if "llm_for_tools_config" in info.data and value.dict(
        ) != info.data["llm_for_tools_config"].dict():
            raise ValueError(
                "At this time llm_for_agents_config to be equal to llm_for_tools_config"
            )
        return value


class AWSConfigurationModel(BaseModel):
    access_key_id: str
    secret_access_key: str


class KOpsConfigurationModel(BaseModel):
    s3_bucket_name: str


class ExperimentModel(BaseModel):
    awx_kubeconfig: str
    awx_chart_version: Optional[str] = None
    aws: AWSConfigurationModel
    git: GitConfigurationModel
    kops: KOpsConfigurationModel
    scenarios: List[int]
    number_of_runs: int = Field(default=20)
    data_modalities: List[str] = Field(default=["metrics", "logs", "traces"])
    agent_configuration: AgentConfigurationModel
    controller_host: Optional[str] = None
    controller_username: Optional[str] = None
    controller_password: Optional[str] = None
