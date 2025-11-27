# UI/UX Refactoring Plan

## 1. Design System & Global Styles (`style.css`)
- **Color Palette**: Refine `--accent-color`, add semantic colors (success, warning, error, surface).
- **Typography**: Define scale for headings (h1-h4), body, caption.
- **Spacing**: Define spacing variables (`--space-xs` to `--space-xl`).
- **Components**:
    - Buttons (Primary, Secondary, Ghost).
    - Cards (Glassmorphism with hover states).
    - Inputs (Focus states, error states).
    - Badges (Status indicators).

## 2. Layout & Navigation (`index.html`, `style.css`)
- **App Bar**: Top bar with Logo, User Status (mock), Help button.
- **Navigation**:
    - Desktop: Sidebar or Top Tabs.
    - Mobile: Bottom Nav or Hamburger Menu.
    - Steps: Profile -> Shortlist -> Requirements -> Timeline.
- **Container**: Responsive container with max-width for readability.

## 3. Onboarding (`index.html`, `app.js`)
- **Welcome Screen**:
    - Hero section with value prop.
    - "How it works" steps (1-2-3).
    - "Start Planning" CTA.
- **State Management**: Simple check in `app.js` to show Welcome vs Main App.

## 4. Forms Refactoring (`index.html`, `app.js`)
- **Stepper**: Break `profileForm` into:
    1.  **Profile**: GPA, Degree, Countries.
    2.  **Preferences**: Budget, Intake, Interests.
    3.  **Scores**: GRE, TOEFL.
- **Validation**: visual feedback on inputs.
- **Mobile Ergonomics**: Ensure 44px+ touch targets.

## 5. Results & Visualization (`app.js`, `style.css`)
- **Program Cards**:
    - Grid layout.
    - Key info badges (Deadline, Tuition).
    - "View Details" action.
- **Timeline View**:
    - Group tasks by Month/Year.
    - Visual connector line.
    - "Next Up" section for immediate tasks.
- **Agent Flow**:
    - Keep existing visualization but integrate it better into the loading state.

## 6. Copy & Tone
- Review all labels.
- Add tooltips for complex terms (e.g., "APS Certificate").

## Execution Order
1.  **Style Foundation**: Update `style.css` with variables and base styles.
2.  **Layout Structure**: Update `index.html` wrapper and nav.
3.  **Onboarding & Form**: Implement Stepper in `index.html` and logic in `app.js`.
4.  **Results Rendering**: Update `renderResults` in `app.js` for new card layout.
5.  **Refinement**: Polish animations and accessibility.
