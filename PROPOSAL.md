# RailNav Pro Phase 1 Proposal

## 1. Executive Summary
RailNav Pro delivers an accessible, voice-first travel companion tailored for blind and low-vision travellers. Phase 1 focuses on delivering a cohesive ecosystem that spans a planning-centric web application, an in-journey Android assistant, and a secure cloud platform coordinated by an AI “brain.” The solution emphasises dependable accessibility, cost-optimised journey planning, and seamless synchronisation so Allan and his carer Jane can plan once and travel confidently across the UK and Europe.

## 2. MVP Scope & Feature Allocation
| Component | Key Responsibilities | Phase 1 Deliverables |
|-----------|----------------------|-----------------------|
| AI Brain  | Multi-modal itinerary research, split-ticketing intelligence, discount optimisation, voice agent | • Integrate commercial LLM (e.g., Gemini 1.5 Pro) via secure API.<br>• Custom prompt/orchestration layer for rail/bus datasets, discount logic, and fallback search hierarchy (rail → bus → plane).<br>• Ticket optimisation engine covering Advance vs. Off-Peak, split tickets, Interrail, National rail passes, and DPRC/carer discounts.<br>• Voice-first conversational layer with context memory for Allan & Jane. |
| Cloud Backend | Authentication, profile storage, trip sync, AI orchestration | • OAuth 2.0 / OpenID Connect authentication (Auth0 or Cognito).<br>• Encrypted storage for user profile (DPRC, carer info, addresses) in managed database (Firebase Firestore or AWS DynamoDB).<br>• REST + WebSocket/FCM APIs for real-time trip sync between web and Android.<br>• Secure audit logging & monitoring.<br>• AI proxy service for rate-limiting, prompt templating, and caching. |
| Web Application | Accessible planning workspace | • Responsive, WCAG 2.2 AA web app using React + TypeScript + Next.js.<br>• Voice command support via Web Speech API + fallback keyboard shortcuts.<br>• Screen-reader-first information architecture (ARIA roles, skip links, focus traps).<br>• Journey builder, fare comparison dashboards, saved trips management.<br>• Passenger Assist auto-fill workflow post-booking. |
| Android Application | In-journey assistant | • Native Kotlin app targeting Android 14 with Jetpack Compose + Accessibility Suite.<br>• Voice interactions via Google Assistant integration and on-device speech recognition.<br>• Offline-ready synced trip storage (Room DB) refreshed via FCM.<br>• Live GPS monitoring with step-free alerts, vibration, and audio prompts.<br>• Passenger Assist auto-fill integration via Android autofill framework + custom tabs.

## 3. Accessibility Strategy (Web & Android)
1. **Voice-first interaction:**
   - Web: Continuous speech recognition toggled by keyboard shortcut or microphone icon; conversational AI responses rendered as screen-reader-friendly cards.
   - Android: Deep links into Assistant + custom wake phrases using App Actions; offline fallback through on-device speech services.
2. **Screen-reader excellence:**
   - Semantic HTML, consistent landmark regions, and extensive ARIA annotations.
   - Compose semantics + TalkBack testing (focus order, content descriptions, haptic cues).
   - Regular audits with NVDA, JAWS, VoiceOver, and TalkBack.
3. **High-contrast, scalable UI:**
   - Dynamic type support, colour-contrast automated linting, reduced motion toggles.
4. **User testing loop:**
   - Bi-weekly usability sessions with Allan and carer persona to validate flows.

## 4. Technical Architecture Overview
- **Hosting:** Cloud provider (AWS or GCP) with managed services (API Gateway, Lambda/Cloud Functions, DynamoDB/Firestore).
- **Data ingestion:** Scheduled ETL jobs pulling rail/bus datasets; integration with NRE Darwin, DB Navigator, SNCF APIs, plus third-party split-ticket providers.
- **AI orchestration:** Server-side agent applying deterministic rules before escalating to LLM for ambiguous cases. Sensitive data masked before LLM calls.
- **Sync pipeline:** REST API for CRUD operations + WebSocket/FCM push updates. Conflict resolution via last-write-wins with change history.
- **Security & compliance:** Encryption at rest (KMS-managed keys), TLS 1.3 in transit, granular IAM roles, audit trails, GDPR-compliant data handling.

## 5. Timeline & Cost Estimate (Phase 1 MVP)
Assuming a 6-person core team (Product, Tech Lead, Accessibility Lead, Backend, Web, Android) plus QA/UX support. Rates in GBP, blended £750/day. Total effort ~72 person-weeks.

| Workstream | Effort (person-weeks) | Duration (calendar) | Cost Estimate |
|------------|-----------------------|---------------------|---------------|
| Discovery & Accessibility Research | 6 | Weeks 1–4 (overlapping) | £22,500 |
| AI Brain (orchestration, datasets, optimisation) | 18 | Weeks 3–14 | £135,000 |
| Cloud Backend & Sync | 16 | Weeks 3–14 | £120,000 |
| Web Application | 14 | Weeks 5–16 | £105,000 |
| Android Application | 14 | Weeks 5–16 | £105,000 |
| QA, Accessibility audits, UAT | 4 | Weeks 12–18 | £30,000 |
| Programme Management & DevOps | 6 | Weeks 1–18 | £45,000 |
| **Total Phase 1 MVP** | **72** | **~18 weeks** | **£562,500** |

### Key Milestones
1. **Weeks 1–4:** Discovery, persona validation, data integration proof-of-concepts, accessibility baseline. Deliver technical architecture doc.
2. **Weeks 5–10:** Core backend + AI orchestration ready; alpha web planner and Android trip viewer; sync prototype.
3. **Weeks 11–14:** Full fare comparison workflows, voice interactions, Passenger Assist auto-fill.
4. **Weeks 15–16:** Beta release with end-to-end journeys, GPS alerts, accessibility audits.
5. **Weeks 17–18:** Hardening, performance, security review, go/no-go.

## 6. Phase 2 High-Level Estimate
| Feature | Scope Highlights | Incremental Effort | Estimate |
|---------|------------------|--------------------|----------|
| Last-mile accessible navigation | Integrate Google Maps/Here Mobility APIs; tactile guidance, indoor mapping pilots. | 10 person-weeks | £56,250 |
| Delay Repay automation | Live disruption monitoring, auto-populated claims, document upload. | 8 person-weeks | £45,000 |
| Calendar integration | Bi-directional sync with Google/Microsoft calendars, sharing with carers. | 4 person-weeks | £22,500 |
| **Total Phase 2 (estimate)** | | **22 person-weeks (~12 weeks calendar)** | **£123,750** |

## 7. Risk Mitigation & Quality Assurance
- **Data availability:** Establish MOUs with rail/bus data providers early; implement caching/fallback suppliers.
- **AI hallucinations:** Guardrail rules, human-readable explanations, and confidence scores; continuous fine-tuning with Allan’s feedback.
- **Accessibility regressions:** Automated axe-core/Accessibility Scanner checks in CI; manual audits each sprint.
- **Security & privacy:** Penetration testing prior to launch; compliance with UK GDPR, data minimisation, and DPIA documentation.

## 8. Next Steps
1. Align on scope, success metrics, and preferred cloud/AI vendors.
2. Kick-off discovery sprint with accessibility workshops and data integration spikes.
3. Finalise Statement of Work and project plan.

RailNav Pro Phase 1 creates a robust foundation for an inclusive, AI-assisted travel experience, ensuring Allan and Jane can plan and travel with confidence while preparing the platform for future enhancements.
