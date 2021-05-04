"""
Mixin for adding created_by and changed_by fields for the instances
"""


class CreateUpdatePreMixin:

    @property
    def request(self):
        return self._context['request']

    def create(self, validated_data):
        validated_data.update({
            'created_by': self.request.user,
            'changed_by': self.request.user
        })
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.update({
            'changed_by': self.request.user
        })
        return super().update(instance, validated_data)
