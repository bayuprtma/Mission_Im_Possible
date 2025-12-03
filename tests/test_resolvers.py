from missionimpossible.resolvers.stack_resolver import resolve_cnn_nlp_stack
from missionimpossible.resolvers.framework_resolver import resolve_framework_stack


def test_framework_resolver_auto():
  stack = resolve_framework_stack(prefer="auto")
  assert isinstance(stack, dict)
  assert any(k in stack for k in ("tensorflow", "torch"))


def test_cnn_nlp_stack_research():
  stack = resolve_cnn_nlp_stack(use_case="research", yolo_family="latest", framework="auto")
  assert isinstance(stack, dict)
  # at least one DL framework + one NLP lib
  assert any(k in stack for k in ("tensorflow", "torch"))
  assert any(k in stack for k in ("nltk", "transformers"))
