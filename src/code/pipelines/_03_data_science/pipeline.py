from kedro.pipeline import Pipeline, node, pipeline

from .nodes import evaluate_model, split_data, train_model


def create_pipeline(**kwargs) -> Pipeline:
    namespace = "modelling_pipeline"
    pipeline_instance =  pipeline(
        [
            node(
                func=split_data,
                inputs=["processing_pipeline.model_input_table", "params:model_options"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data",
            ),
            node(
                func=train_model,
                inputs=["X_train", "y_train"],
                outputs="regressor",
                name="train_model",
            ),
            node(
                func=evaluate_model,
                inputs=["regressor", "X_test", "y_test"],
                name="evaluate_model",
                outputs="metrics",
            ),
        ]
    )
    ds_pipeline_1 = pipeline(
        pipe=pipeline_instance,
        inputs="processing_pipeline.model_input_table",
        parameters="model_options",
        namespace="active_modelling_pipeline",
    )
    ds_pipeline_2 = pipeline(
        pipe=pipeline_instance,
        inputs="processing_pipeline.model_input_table",
        parameters="model_options",
        namespace="candidate_modelling_pipeline",
    )

    return ds_pipeline_1 + ds_pipeline_2

