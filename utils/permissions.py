from rest_framework import permissions

class IsAdminOrInstructorForSession(permissions.BasePermission):
    """
    Custom permission to allow only admins and the course instructor
    to add students to a session.
    """

    def has_permission(self, request, view):
        # Allow access if the user is an admin
        if request.user and request.user.is_staff:
            return True
        return True  # Defer object-level checks to `has_object_permission`

    def has_object_permission(self, request, view, obj):
        # Allow access if the user is the instructor of the course for the session
        print("obj.course.instructor=",obj.course.instructor.user)
        return obj.course.instructor.user == request.user
