import React, { useState, useEffect } from 'react';
import { getReminders } from '../services/reminderService';

function Reminder() {
  const [reminders, setReminders] = useState([]);

  useEffect(() => {
    // Fetch reminders from backend API
    const fetchReminders = async () => {
      const remindersData = await getReminders();
      setReminders(remindersData);
    };

    fetchReminders();
  }, []);

  return (
    <div>
      <h2>Reminders</h2>

      {reminders.map((reminder) => (
        <div key={reminder.id}>
          <div>{reminder.title}</div>
          <div>{reminder.description}</div>
          <div>{reminder.date}</div>
        </div>
      ))}
    </div>
  );
}

export default Reminder;
