
def get_pks_to_delete(instance_fulfill, updated_fulfill):
    instance_pks = set((x['id'] for x in instance_fulfill
                        if 'id' in x.keys()))
    updated_pks = set((x['id'] for x in updated_fulfill
                        if 'id' in x.keys()))
    return list(instance_pks.symmetric_difference(updated_pks))



