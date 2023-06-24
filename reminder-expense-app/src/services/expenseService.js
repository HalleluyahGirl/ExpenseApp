export async function getExpenses() {
    try {
      const response = await fetch('/api/expenses');
      const data = await response.json();
      return data.expenses;
    } catch (error) {
      console.error('Error fetching expenses:', error);
      return [];
    }
  }
  