from rest_framework import permissions


class IsAnonymous(permissions.BasePermission):
	message = 'You are already logged'

	def has_permission(self, request, view):
		print(request.user)
		return not request.user.is_authenticated

