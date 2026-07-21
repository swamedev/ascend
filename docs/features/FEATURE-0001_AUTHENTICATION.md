# FEATURE-0001 — Authentication

> **Status:** Draft  
> **Author:** Chief Architect  
> **Date:** 2026-07-20  
> **Phase:** E  
> **Depends on:** Experience Freeze v1.0, Frontend SDK (mocked)

---

## 1. Objective

Deliver a complete authentication experience: login, logout, session persistence, route guards, and user identity display.

---

## 2. Scope

- Login screen (email + password)
- Logout action (from any authenticated page)
- Session token storage (local storage, SDK-managed)
- Route guard (redirect unauthenticated users to `/login`)
- User menu (avatar + name + logout in TopBar)
- Loading, error, and idle states for auth flow

---

## 3. Out of Scope

- Registration / sign-up
- Password reset / forgot password
- OAuth / social login
- MFA / 2FA
- Role-based access control (RBAC) — *deferred to post-MVP*
- Session refresh / silent renewal — *deferred*

---

## 4. User Flows

### Flow A — Login

```
User opens /login
  → Sees email + password form
  → Fills credentials
  → Clicks "Sign In"
  → [Loading] button shows spinner
  → [Success] redirect to /dashboard
  → [Error] inline error message, form stays
```

### Flow B — Logout

```
User clicks avatar in TopBar
  → User Menu dropdown opens
  → Clicks "Sign Out"
  → Session cleared
  → Redirect to /login
```

### Flow C — Unauthenticated Access

```
User navigates to /dashboard (or any protected route)
  → Guard checks session
  → No session found
  → Redirect to /login with returnUrl
  → After login, redirect back to original URL
```

### Flow D — Session Restore

```
User refreshes page while authenticated
  → App loads
  → AuthProvider reads token from SDK
  → If valid, restore session → show authenticated layout
  → If invalid/expired, clear → redirect to /login
```

---

## 5. Components Used

| Component | Usage |
|-----------|-------|
| `PageContainer` | Login page wrapper |
| `Card`, `CardHeader`, `CardContent` | Login form card |
| `Input` | Email and password fields |
| `Label` | Field labels |
| `Button` | Sign In / Sign Out |
| `IconButton` | — |
| `Spinner` | Loading state in button |
| `Badge` | — |
| `Avatar` | User avatar in TopBar |
| `Divider` | — |
| `Alert` | Error display on login |
| `TopBar`, `TopBarAction` | User menu trigger |
| `LoadingState` | Auth check on page load |
| `ErrorState` | Auth error fallback |

---

## 6. States

| State | Screen | Visual |
|-------|--------|--------|
| `idle` | `/login` | Empty form, "Sign In" enabled |
| `loading` | `/login` | Button shows spinner, fields disabled |
| `error` | `/login` | Alert box with error message |
| `authenticated` | Dashboard | User menu visible, TopBar shows avatar |
| `unauthenticated` | Any protected route | Redirect to `/login?returnUrl=...` |
| `checking` | App root | `LoadingState` while reading session |
| `session_expired` | Any protected route | Clear session → redirect to `/login` |

---

## 7. Events

| Event | Trigger | Effect |
|-------|---------|--------|
| `auth:login:start` | User submits form | Button → loading, fields disabled |
| `auth:login:success` | API returns 200 | Token stored in SDK, redirect to dashboard |
| `auth:login:error` | API returns error | Alert shown, button re-enabled |
| `auth:logout` | User clicks "Sign Out" | Session cleared, redirect to /login |
| `auth:session:restored` | Page refresh, valid token | Authenticated layout rendered |
| `auth:session:expired` | Token invalid/missing | Clear session, redirect to /login |

---

## 8. Required Data

```typescript
interface LoginRequest {
  email: string
  password: string
}

interface LoginResponse {
  token: string
  user: UserProfile
}

interface UserProfile {
  id: string
  name: string
  email: string
  avatar?: string
  level: number
  xp: number
}
```

---

## 9. API Contracts (Mocked)

### POST /api/auth/login

```
Request:  { email: string, password: string }
Success:  { token: string, user: UserProfile }
Error:    { error: "Invalid credentials" }
Status:   200 | 401
```

### POST /api/auth/logout

```
Request:  (empty)
Success:  { ok: true }
Status:   200
```

### GET /api/auth/session

```
Request:  Authorization: Bearer <token>
Success:  { valid: true, user: UserProfile }
Error:    { valid: false }
Status:   200 | 401
```

---

## 10. Acceptance Criteria

- [ ] User can log in with valid credentials
- [ ] Incorrect credentials show inline error, not redirect
- [ ] After login, user is redirected to the originally requested page
- [ ] User menu shows avatar and name when authenticated
- [ ] "Sign Out" clears session and redirects to login
- [ ] Refreshing the page restores session (if token is valid)
- [ ] Unauthenticated users cannot access protected routes
- [ ] All states (idle, loading, error, checking) are visually represented
- [ ] Login form is keyboard-accessible (Tab, Enter to submit)
- [ ] Works in light and dark mode

---

## 11. Error Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Wrong email/password | Alert: "Invalid email or password" |
| Network timeout | Alert: "Connection error. Please try again." |
| Expired session | Auto-redirect to /login |
| Empty form submission | Inline validation: "Email is required" / "Password is required" |
| Server error (500) | Alert: "Something went wrong. Please try again." |

---

## 12. Expected Tests

```
auth/
  LoginPage.test.tsx
    - renders form fields
    - shows validation errors for empty fields
    - calls login API on submit
    - shows loading state during request
    - shows error alert on failure
    - redirects to dashboard on success
    - redirects to returnUrl after login
  
  UserMenu.test.tsx
    - renders avatar with user initials
    - opens dropdown on click
    - shows "Sign Out" option
    - calls logout on click
  
  AuthGuard.test.tsx
    - redirects to /login if unauthenticated
    - renders children if authenticated
    - shows LoadingState while checking
```
