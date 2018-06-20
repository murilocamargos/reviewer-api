from rest_framework import serializers, validators

from review import models


class CompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)

    class Meta:
        model = models.Company
        fields = ('id', 'name', )

'''
class PolicySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    start_at = serializers.TimeField()
    finish_at = serializers.TimeField()
    standing_price = serializers.DecimalField(max_digits=5, decimal_places=2)
    variable_price = serializers.DecimalField(max_digits=5, decimal_places=2)

    @staticmethod
    def validate_time(time, instance, finish=False):
        """
        Checks if given time is inside some price policy interval.
        """
        if finish:
            time = datetime.time(time.hour - 1, 59, 59)

        check_intervals = models.Policy.objects.filter(
            (
                Q(
                    start_at__lte=time,
                    finish_at__gt=time,
                ) & Q(
                    start_at__lte=F('finish_at')
                )
            ) | (
                Q(
                    Q(start_at__lte=time) |
                    Q(finish_at__gt=time)
                ) & Q(
                    start_at__gt=F('finish_at')
                )
            )
        )

        if instance:
            check_intervals = check_intervals.exclude(id=instance.id)
            
        if check_intervals.exists():
            msg = "There is already an interval covering this time."
            raise serializers.ValidationError(msg)

    def validate_start_at(self, value):
        """
        We can't have two price policies for the same time.
        """
        self.validate_time(value, self.instance)
        return value

    def validate_finish_at(self, value):
        """
        We can't have two price policies for the same time.
        """
        self.validate_time(value, self.instance, True)
        return value

    class Meta:
        model = models.Policy
        fields = ('id', 'name', 'start_at', 'finish_at', 'standing_price',
                  'variable_price', )


class CallSerializer(serializers.ModelSerializer):
    caller = serializers.PrimaryKeyRelatedField(
        queryset=models.Subscriber.objects.all()
    )
    callee = serializers.PrimaryKeyRelatedField(
        queryset=models.Subscriber.objects.all()
    )
    start_at = serializers.DateTimeField(required=False)
    finish_at = serializers.DateTimeField(required=False, allow_null=True)
    price = serializers.DecimalField(max_digits=20, decimal_places=2,
                                     read_only=True)

    @staticmethod
    def validate_dates(start_at, finish_at):
        """
        Validates the call's start and finish time.
        """
        msg = None
        if start_at > finish_at:
            msg = "You can finish the call before starting it."

        if (finish_at - start_at).total_seconds() / 3600 > 48:
            msg = "The maximum duration of a call is 48h."

        if msg:
            raise serializers.ValidationError({
                'finish_at': [msg]
            })

    def validate(self, data):
        """
        Validates the call's data.
        """
        if data.get('finish_at') and data.get('start_at'):
            self.validate_dates(data.get('start_at'), data.get('finish_at'))
        
        if data.get('caller') and data.get('caller') == data.get('callee'):
            msg = "Subscribers can't call to themselves."
            raise serializers.ValidationError({
                'callee': [msg]
            })

        return data

    def create(self, validated_data):
        """
        At the call creation, we're only interested in the caller, callee and
        the start time.
        """
        # Remove unwanted fields
        if 'finish_at' in validated_data:
            validated_data.pop('finish_at')

        if 'price' in validated_data:
            validated_data.pop('price')

        # Checks if start_at fields came
        if 'start_at' not in validated_data:
            validated_data['start_at'] = timezone.now()

        return models.Call.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Checks if start_at fields came
        if 'finish_at' not in validated_data:
            validated_data['finish_at'] = timezone.now()

        finish_at = validated_data.get('finish_at')

        self.validate_dates(instance.start_at, finish_at)

        instance.finish_at = finish_at
        instance.save()
        return instance

    class Meta:
        model = models.Call
        fields = ('id', 'caller', 'callee', 'start_at', 'finish_at',
                  'price', )


class SubscriberBillCallSerializer(serializers.Serializer):
    callee = serializers.PrimaryKeyRelatedField(read_only=True)
    start_at = serializers.DateTimeField()
    finish_at = serializers.DateTimeField()
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    duration = serializers.CharField()


class SubscriberBillSerializer(serializers.Serializer):
    cycle_begin = serializers.DateTimeField()
    cycle_end = serializers.DateTimeField()
    total = serializers.DecimalField(max_digits=5, decimal_places=2)
    calls = SubscriberBillCallSerializer(
        many=True,
        read_only=True,
        source='calls_made_in',
    )
'''