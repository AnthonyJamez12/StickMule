#Imports


@api_view(['GET'])
def readUserPoolMembershipList(request, pool_id):
    try:
        user_profile = request.user.profile  # Assuming you're using authentication
        user_location = user_profile.location
    except Profile.DoesNotExist:
        return Response(status=404)

    # Ensure user has a valid location
    if user_location.x == 0.0 and user_location.y == 0.0:
        return Response(status=400, data={"message": "Invalid user location"})

    radius_miles = 50

    # Retrieve users who have joined the specific pool
    users_in_pool = Profile.objects.exclude(location__isnull=True).filter(
        memberships__pool_id=pool_id
    )

    # Filter those users based on distance
    users_within_radius = users_in_pool.filter(
        location__distance_lte=(user_location, Distance(mi=radius_miles))
    ).exclude(user=user_profile.user)

    serializer = ProfileSerializer(users_within_radius, many=True)
    return Response(serializer.data)
