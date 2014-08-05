from tastypie.resources import ModelResource


class MyBaseResource(ModelResource):
    def determine_format(self, request):
        '''Return JSON by default'''
        return 'application/json'
