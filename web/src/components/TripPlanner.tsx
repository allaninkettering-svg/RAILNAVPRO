import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import client, { login } from '../api/client';
import { LiveMessage } from 'react-aria-live';

type SegmentMode = 'train' | 'bus' | 'plane';

type Segment = {
  mode: SegmentMode;
  origin: string;
  destination: string;
  departure_time: string;
  arrival_time: string;
  service_number?: string;
  accessibility_notes: string;
};

type PlannerState = {
  email: string;
  token?: string;
  title: string;
  segments: Segment[];
  fareTotal: number;
  notes: string;
  passengerAssist: 'yes' | 'no';
  liveMessage: string;
};

const defaultState: PlannerState = {
  email: '',
  title: '',
  segments: [
    {
      mode: 'train',
      origin: '',
      destination: '',
      departure_time: '',
      arrival_time: '',
      service_number: '',
      accessibility_notes: ''
    }
  ],
  fareTotal: 0,
  notes: '',
  passengerAssist: 'yes',
  liveMessage: ''
};

const TripPlanner: React.FC = () => {
  const [state, setState] = useState<PlannerState>(defaultState);

  const loginMutation = useMutation({
    mutationFn: (email: string) => login(email),
    onSuccess: (data) => {
      setState((prev) => ({
        ...prev,
        token: data.access_token,
        liveMessage: `Signed in as ${data.user.name}`
      }));
    },
    onError: () => {
      setState((prev) => ({
        ...prev,
        liveMessage: 'We could not sign you in. Please check your email address.'
      }));
    }
  });

  const saveTripMutation = useMutation({
    mutationFn: async () => {
      if (!state.token) {
        throw new Error('Please sign in first.');
      }
      const response = await client.post(
        '/trips',
        {
          title: state.title,
          segments: state.segments.map((segment) => ({
            ...segment,
            accessibility_notes: segment.accessibility_notes
              ? segment.accessibility_notes.split('\n')
              : []
          })),
          fare: {
            currency: 'GBP',
            total: state.fareTotal,
            components: ['Draft fare estimate']
          },
          passenger_assist_requested: state.passengerAssist === 'yes',
          notes: state.notes
        },
        {
          headers: {
            Authorization: `Bearer ${state.token}`
          }
        }
      );
      return response.data;
    },
    onSuccess: () => {
      setState((prev) => ({
        ...defaultState,
        email: prev.email,
        token: prev.token,
        liveMessage: 'Trip saved to the cloud and ready for Android sync.'
      }));
    },
    onError: (error: unknown) => {
      const message = error instanceof Error ? error.message : 'Unable to save trip.';
      setState((prev) => ({
        ...prev,
        liveMessage: message
      }));
    }
  });

  const updateSegment = (
    index: number,
    field: keyof Segment,
    value: string | SegmentMode
  ) => {
    setState((prev) => {
      const segments = [...prev.segments];
      segments[index] = { ...segments[index], [field]: value };
      return { ...prev, segments };
    });
  };

  return (
    <section aria-labelledby="planner-heading">
      <LiveMessage message={state.liveMessage} aria-live="polite" />
      <h2 id="planner-heading">Create a new journey</h2>
      <p>
        Provide details for each segment. The Android app will replay these steps with
        GPS-triggered prompts.
      </p>

      <form
        onSubmit={(event) => {
          event.preventDefault();
          saveTripMutation.mutate();
        }}
      >
        <fieldset>
          <legend>Step 1 – Sign in</legend>
          <label htmlFor="email-input">Email address</label>
          <input
            id="email-input"
            type="email"
            autoComplete="email"
            required
            value={state.email}
            onChange={(event) => setState({ ...state, email: event.target.value })}
          />
          <button
            type="button"
            onClick={() => loginMutation.mutate(state.email)}
            aria-describedby="login-help"
            disabled={loginMutation.isLoading || !state.email}
          >
            {loginMutation.isLoading ? 'Signing in…' : 'Generate secure link'}
          </button>
          <p id="login-help">
            We use a one-time passcode sent to your email. During the MVP we auto-fill the
            passcode.
          </p>
        </fieldset>

        <fieldset>
          <legend>Step 2 – Journey overview</legend>
          <label htmlFor="title-input">Trip title</label>
          <input
            id="title-input"
            value={state.title}
            onChange={(event) => setState({ ...state, title: event.target.value })}
            required
          />
          <label htmlFor="fare-total">Estimated total fare (£)</label>
          <input
            id="fare-total"
            type="number"
            min="0"
            step="0.01"
            value={state.fareTotal}
            onChange={(event) =>
              setState({ ...state, fareTotal: Number(event.target.value) })
            }
            required
          />
          <label htmlFor="notes-input">Notes for Allan and Jane</label>
          <textarea
            id="notes-input"
            rows={3}
            value={state.notes}
            onChange={(event) => setState({ ...state, notes: event.target.value })}
          />
          <fieldset>
            <legend>Passenger Assist</legend>
            <div role="radiogroup" aria-labelledby="assist-group">
              <span id="assist-group" className="sr-only">
                Would you like Passenger Assist booked?
              </span>
              <label>
                <input
                  type="radio"
                  name="assist"
                  value="yes"
                  checked={state.passengerAssist === 'yes'}
                  onChange={() => setState({ ...state, passengerAssist: 'yes' })}
                />
                Yes, request assistance
              </label>
              <label>
                <input
                  type="radio"
                  name="assist"
                  value="no"
                  checked={state.passengerAssist === 'no'}
                  onChange={() => setState({ ...state, passengerAssist: 'no' })}
                />
                No assistance needed
              </label>
            </div>
          </fieldset>
        </fieldset>

        <fieldset>
          <legend>Step 3 – Segments</legend>
          {state.segments.map((segment, index) => (
            <div key={index} className="segment-card">
              <h3>Segment {index + 1}</h3>
              <label htmlFor={`segment-mode-${index}`}>Mode</label>
              <select
                id={`segment-mode-${index}`}
                value={segment.mode}
                onChange={(event) =>
                  updateSegment(index, 'mode', event.target.value as SegmentMode)
                }
              >
                <option value="train">Train</option>
                <option value="bus">Bus</option>
                <option value="plane">Plane</option>
              </select>

              <label htmlFor={`origin-${index}`}>Origin station</label>
              <input
                id={`origin-${index}`}
                value={segment.origin}
                onChange={(event) => updateSegment(index, 'origin', event.target.value)}
                required
              />

              <label htmlFor={`destination-${index}`}>Destination station</label>
              <input
                id={`destination-${index}`}
                value={segment.destination}
                onChange={(event) =>
                  updateSegment(index, 'destination', event.target.value)
                }
                required
              />

              <label htmlFor={`departure-${index}`}>Departure time</label>
              <input
                id={`departure-${index}`}
                type="datetime-local"
                value={segment.departure_time}
                onChange={(event) =>
                  updateSegment(index, 'departure_time', event.target.value)
                }
                required
              />

              <label htmlFor={`arrival-${index}`}>Arrival time</label>
              <input
                id={`arrival-${index}`}
                type="datetime-local"
                value={segment.arrival_time}
                onChange={(event) =>
                  updateSegment(index, 'arrival_time', event.target.value)
                }
                required
              />

              <label htmlFor={`service-${index}`}>Service number</label>
              <input
                id={`service-${index}`}
                value={segment.service_number}
                onChange={(event) =>
                  updateSegment(index, 'service_number', event.target.value)
                }
              />

              <label htmlFor={`notes-${index}`}>
                Accessibility notes (one per line for screen reader prompts)
              </label>
              <textarea
                id={`notes-${index}`}
                rows={3}
                value={segment.accessibility_notes}
                onChange={(event) =>
                  updateSegment(index, 'accessibility_notes', event.target.value)
                }
              />
            </div>
          ))}
        </fieldset>

        <button type="submit" disabled={saveTripMutation.isLoading}>
          {saveTripMutation.isLoading ? 'Saving…' : 'Save to cloud'}
        </button>
      </form>
    </section>
  );
};

export default TripPlanner;
