.PHONY: update_schemas server_schemas agent_schemas client_schemas clean_schemas

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
				--output "$(1)/$$(basename "$$file" .json).py"; \
		done;

COPY_INIT = @cp ./schemas/__init__.py $(1)/__init__.py; \
            cp ./schemas/__init__.py $(1)/codegen/__init__.py;

update_schemas: clean_schemas server_schemas agent_schemas client_schemas

clean_schemas:
	@echo "Cleaning schema directories..."
	@rm -f ../{agent,client,server}/schemas/*.py
	@rm -f ../{agent,client,server}/schemas/codegen/*.py

server_schemas:
	@echo "Updating Python models for server..."
	$(call GENERATE_MODELS,../server/schemas/codegen/)
	$(call COPY_INIT,../server/schemas)
	@cp ./schemas/*.py ../server/schemas/

agent_schemas:
	@echo "Updating Python models for agent..."
	$(call GENERATE_MODELS,../agent/schemas/codegen/)
	$(call COPY_INIT,../agent/schemas)
	@cp ./schemas/*.py ../agent/schemas/

client_schemas:
	@echo "Updating Python models for client..."
	$(call GENERATE_MODELS,../client/schemas/codegen/)
	$(call COPY_INIT,../client/schemas)
	@cp ./schemas/*.py ../client/schemas/
