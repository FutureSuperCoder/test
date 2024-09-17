from django.db.models import Count, Case, When, IntegerField

def check_numbers_exist(numbers):
    # 构造一个查询，返回所有 number 及其对应的存在状态
    number_exists = MyModel.objects.filter(number__in=numbers).values('number') \
        .annotate(exists=Count('id')) \
        .values_list('number', 'exists')

    # 将查询结果转为字典
    result_dict = {number: True for number, exists in number_exists}

    # 构造最终的结果，检查每个传入的 number 是否存在
    return {number: result_dict.get(number, False) for number in numbers}



from django.db.models import Q, Case, When, Value, BooleanField

def query_with_grouped_results(numbers):
    # 使用 Q 对象结合 __in 查询多个 number
    query = Q(number__in=numbers)
    
    # 执行查询，并对每个 number 标记是否存在
    results = MyModel.objects.filter(query).values('number').annotate(
        exists=Case(
            When(number__in=numbers, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        )
    )
    
    # 构造一个字典，标记每个 number 的查询结果
    result_dict = {result['number']: result['exists'] for result in results}
    
    # 补全没有返回的 number，标记为不存在
    return {number: result_dict.get(number, False) for number in numbers}

