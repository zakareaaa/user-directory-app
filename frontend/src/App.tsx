import { useQuery } from "@tanstack/react-query";
import './App.css'

type User = {
  id: number;
  name: string;
  email: string;
  created_at: string;
  updated_at: string;
};


async function fetchUsers(): Promise<User[]> {
  const response = await fetch("http://localhost:8000/users");

  if (!response.ok) {
    throw new Error("Failed to fetch users");
  }

  return response.json();
}






function App() {
  const { data, error, isFetching, refetch } = useQuery({
    queryKey: ["users"],
    queryFn: fetchUsers,
    enabled: false,
  });

  return (
    <main>
      <h1>User Directory</h1>

      <button onClick={() => refetch()} disabled={isFetching}>
        {isFetching ? "Loading..." : "Fetch Users"}
      </button>

      {error && <p className="error-message">Could not load users.</p>}

      {data?.map((user) => (
        <article key={user.id}>
          <h2>{user.name}</h2>
          <p>{user.email}</p>
        </article>
      ))}
    </main>
  );
}

export default App;