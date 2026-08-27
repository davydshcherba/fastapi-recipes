import { useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL ?? '/api'

type Recipe = {
  id: number
  title: string
  cuisine: string | null
  servings: number
  ingredients: string[]
  steps: string[]
  owner_id: number
  created_at: string
}

function App() {
  const [ingredients, setIngredients] = useState('')
  const [token, setToken] = useState(
    () => localStorage.getItem('token') ?? '',
  )
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [recipe, setRecipe] = useState<Recipe | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setRecipe(null)

    const list = ingredients
      .split(/[\n,]/)
      .map((s) => s.trim())
      .filter(Boolean)

    if (list.length === 0) {
      setError('Введи хоча б один інгредієнт')
      return
    }

    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/create-recipe-ai`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify(list),
      })

      if (!res.ok) {
        const detail = await res.text()
        throw new Error(`${res.status}: ${detail}`)
      }

      setRecipe((await res.json()) as Recipe)
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4">
      <div className="mx-auto max-w-2xl">
        <h1 className="text-3xl font-semibold text-slate-900">
          Рецепт з інгредієнтів
        </h1>
        <p className="mt-2 text-slate-600">
          Введи інгредієнти через кому або з нового рядка — бек згенерує рецепт.
        </p>

        <form
          onSubmit={handleSubmit}
          className="mt-6 space-y-4 rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
        >
          <label className="block">
            <span className="text-sm font-medium text-slate-700">
              Інгредієнти
            </span>
            <textarea
              value={ingredients}
              onChange={(e) => setIngredients(e.target.value)}
              rows={4}
              placeholder="курка, рис, помідори"
              className="mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900 outline-none focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
            />
          </label>

          <label className="block">
            <span className="text-sm font-medium text-slate-700">
              Access token
            </span>
            <input
              type="password"
              value={token}
              onChange={(e) => {
                setToken(e.target.value)
                localStorage.setItem('token', e.target.value)
              }}
              placeholder="Bearer JWT з /login"
              className="mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900 outline-none focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
            />
          </label>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-slate-900 px-4 py-2 font-medium text-white transition hover:bg-slate-800 disabled:opacity-50"
          >
            {loading ? 'Генеруємо…' : 'Згенерувати рецепт'}
          </button>

          {error && (
            <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
              {error}
            </p>
          )}
        </form>

        {recipe && (
          <article className="mt-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-2xl font-semibold text-slate-900">
              {recipe.title}
            </h2>
            <p className="mt-1 text-sm text-slate-500">
              {recipe.cuisine ?? 'Кухня не вказана'} · {recipe.servings} порцій
            </p>

            <h3 className="mt-4 font-medium text-slate-800">Інгредієнти</h3>
            <ul className="mt-1 list-inside list-disc text-slate-700">
              {recipe.ingredients.map((it, i) => (
                <li key={i}>{it}</li>
              ))}
            </ul>

            <h3 className="mt-4 font-medium text-slate-800">Кроки</h3>
            <ol className="mt-1 list-inside list-decimal space-y-1 text-slate-700">
              {recipe.steps.map((step, i) => (
                <li key={i}>{step}</li>
              ))}
            </ol>
          </article>
        )}
      </div>
    </div>
  )
}

export default App
