from apps import model_choices as mch

def global_context(request):
    return {'mch': mch}