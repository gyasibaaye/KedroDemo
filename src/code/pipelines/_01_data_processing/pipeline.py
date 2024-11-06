from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_model_input_table, preprocess_companies, preprocess_shuttles


def create_pipeline(**kwargs) -> Pipeline: 
    pipeline_instance = pipeline(
        [
            node(
                func=preprocess_companies,
                inputs="companies",
                outputs=["preprocessed_companies", "companies_columns"],
                name="preprocess_companies_node",
            ),
            node(
                func=preprocess_shuttles,
                inputs="shuttles",
                outputs="preprocessed_shuttles",
                name="preprocess_shuttles_node",
            ),
            node(
                func=create_model_input_table,
                inputs=["preprocessed_shuttles", "preprocessed_companies", "reviews"],
                outputs="model_input_table",
                name="create_model_input_table_node",
            ),
        ]
    )
    processing_pipeline_1 = pipeline(
        pipe=pipeline_instance,
        inputs=["companies", "shuttles", "reviews"],
        # parameters="",
        namespace="processing_pipeline",
    )

    return processing_pipeline_1
