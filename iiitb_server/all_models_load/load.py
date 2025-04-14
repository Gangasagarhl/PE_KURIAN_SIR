from all_models_load import blip,t5
def load():
    blp = blip.blip_load()
    t= t5.t5_load()
    print("status: ", blp.is_ready and t.is_ready)