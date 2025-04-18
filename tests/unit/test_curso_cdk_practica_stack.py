import aws_cdk as core
import aws_cdk.assertions as assertions

from curso_cdk_practica.curso_cdk_practica_stack import CursoCdkPracticaStack

# example tests. To run these tests, uncomment this file along with the example
# resource in curso_cdk_practica/curso_cdk_practica_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CursoCdkPracticaStack(app, "curso-cdk-practica")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
