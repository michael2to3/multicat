.PHONY: update_schemas server_schemas agent_schemas client_schemas clean_schemas agent_init_commands

GENERATE_MODELS = @for file in ./schemas/*.json; do \
                    datamodel-codegen \
				--target-python-version 3.11 \
				--use-schema-description \
				--use-default \
				--collapse-root-models \
				--use-double-quotes \
				--output-model-type pydantic_v2.BaseModel \
				--strict-nullable \
				--field-constraints \
				--disable-timestamp \
				--use-subclass-enum \
				--extra-template-data ./template/extra.json \
				--input-file-type jsonschema \
				--input "$$file" \
				--output "$(1)/codegen/$$(basename "$$file" .json).py"; \
		done;

GENERATE_INIT = mkinit "$(1)/codegen/" --recursive -w --black --relative && \
	mkinit "$(1)" --recursive -w --black --relative;

COPY_MODELS = cp ./schemas/*.py "$(1)" && \
	      cp ./schemas/__init__.py "$(1)/codegen/";

GENERATE_ALL = $(call GENERATE_MODELS,$(1)) \
	$(call COPY_MODELS,$(1)) \
	$(call GENERATE_INIT,$(1))

GENERATE_INIT_COMMANDS = @mkinit "../agent/commands/" --recursive -w --black --relative --nomods;

all: update_schemas agent_init_commands

update_schemas: clean_schemas server_schemas agent_schemas client_schemas

clean_schemas:
	@echo "Cleaning schema directories..."
	@rm -f ../{agent,client,server}/schemas/*.py
	@rm -f ../{agent,client,server}/schemas/codegen/*.py

server_schemas:
	@echo "Updating Python models for server..."
	$(call GENERATE_ALL,../server/schemas/)

agent_schemas:
	@echo "Updating Python models for agent..."
	$(call GENERATE_ALL,../agent/schemas/)

agent_init_commands:
	@echo "Updating Init for commands bot"
	$(call GENERATE_INIT_COMMANDS)

client_schemas:
	@echo "Updating Python models for client..."
	$(call GENERATE_ALL,../client/schemas/)
