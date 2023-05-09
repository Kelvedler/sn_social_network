def get_request_ip(request):
    ips = request.META.get('HTTP_X_FORWARDED_FOR', None)
    return ips.split(',')[0] if ips else request.META.get('REMOTE_ADDR', None)
