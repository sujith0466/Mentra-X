import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "@/store/useAuthStore";

interface ProtectedRouteProps {
  allowedRoles?: Array<"student" | "admin" | string>;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ allowedRoles }) => {
  const { user } = useAuthStore();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && allowedRoles.length > 0 && !allowedRoles.includes(user.role)) {
    // Role mismatch: redirect user to their authorized home portal
    const homeRedirect = user.role === "admin" ? "/admin/dashboard" : "/student/dashboard";
    return <Navigate to={homeRedirect} replace />;
  }

  return <Outlet />;
};
