from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    compare_passenger_capacity_exp,
    compare_passenger_capacity_go,
    create_confusion_matrix,
    create_actual_predicted_plot,
)


def create_pipeline(**kwargs) -> Pipeline:
    """This is a simple pipeline which generates a pair of plots"""
    namespace = "reporting_pipeline"
    pipeline_instance = pipeline(
        [
            node(
                func=compare_passenger_capacity_exp,
                inputs="processing_pipeline.preprocessed_shuttles",
                outputs="shuttle_passenger_capacity_plot_exp",
                # namespace=namespace
            ),
            node(
                func=compare_passenger_capacity_go,
                inputs="processing_pipeline.preprocessed_shuttles",
                outputs="shuttle_passenger_capacity_plot_go",
                # namespace=namespace
            ),
            node(
                func=create_confusion_matrix,
                inputs="companies",
                outputs="dummy_confusion_matrix",
                # namespace=namespace
            ),
            node(
                func=create_actual_predicted_plot,
                inputs=["active_modelling_pipeline.X_test", "active_modelling_pipeline.y_test","active_modelling_pipeline.regressor"],
                outputs="actual_predicted_plot",
            )
        ]
    )
    reporting_pipeline_1 = pipeline(
        pipe=pipeline_instance,
        inputs=[
            "active_modelling_pipeline.X_test",
            "active_modelling_pipeline.y_test",
            "active_modelling_pipeline.regressor",
            "processing_pipeline.preprocessed_shuttles",
            "companies"
            ],
        # parameters="",
        namespace="reporting_pipeline",
    )
    return reporting_pipeline_1
