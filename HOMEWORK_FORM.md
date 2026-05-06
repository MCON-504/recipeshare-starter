# Homework: Add a Recipe Review Form to RecipeShare

## Goal

In this homework, you will add a small but realistic feature to the RecipeShare application: **recipe reviews**.

A logged-in user should be able to visit a recipe detail page, open a review form, submit a rating and a short comment, and save that review in the database.

This assignment is designed to practice wiring together the full Flask form pattern:

1. Add a small SQLAlchemy model.
2. Generate and apply a database migration.
3. Add a Flask-WTF form class.
4. Add a route that handles both `GET` and `POST`.
5. Render a template with fields, errors, CSRF protection, and a submit button.
6. Connect the saved review to the current user and the recipe being reviewed.

You should use the lesson examples as a guide, but you should write the Python logic yourself.

---

## Feature: Recipe Reviews

Each review belongs to:

- one recipe
- one logged-in user

Each review should contain:

- a numeric rating
- a short written comment
- a timestamp showing when the review was created

This is a good feature for RecipeShare because it extends the app in a natural way. Recipes are public content, and reviews let users respond to recipes without editing the recipe itself.

---

## Files You Will Modify

You should place your work in the existing application files:

| File | What to add |
|---|---|
| `app/models.py` | Add a `RecipeReview` model |
| `app/forms.py` | Add a `RecipeReviewForm` class |
| `app/routes.py` | Add a route for creating a review |
| `templates/recipes/review_form.html` | Add the provided template |

Depending on the current structure of your project, your templates folder may be named slightly differently. Use the folder structure already used by your app.

---

## Part 1: Add the Model

Add a new SQLAlchemy model named `RecipeReview` to `app/models.py`.

The model should represent one review written by one user for one recipe.

### Required fields

Your model should include the following fields:

| Field | Type / Requirement | Purpose |
|---|---|---|
| `id` | Integer primary key | Unique ID for the review |
| `rating` | Integer, required | Rating from 1 to 5 |
| `comment` | String or Text, required | Short written review |
| `created_at` | DateTime | When the review was created |
| `recipe_id` | Foreign key to recipe | The recipe being reviewed |
| `user_id` | Foreign key to user | The user who wrote the review |

### Relationship guidance

The review should connect to both the `Recipe` model and the `User` model.

Think through these questions before writing the model:

- Can one recipe have many reviews?
- Can one user write many reviews?
- Does each review belong to exactly one recipe?
- Does each review belong to exactly one user?

Your relationships should make it easy to access:

- all reviews for a recipe
- the user who wrote a review
- the recipe that a review belongs to

### Validation note

The database model can store the data, but the form will handle most user-facing validation. The form should prevent ratings outside the allowed range before the model is saved.

---

## Part 2: Create and Apply a Migration

After adding the model, you need to update the database schema.

If the project uses Flask-Migrate, follow this process from the project root.

### Step 1: Confirm the app can load

Before creating a migration, make sure the app starts without import errors.

You can run the app normally or use a Flask command to confirm Flask can discover the application.

If Flask cannot import your app, fix that first. Migration commands depend on the application loading correctly.

### Step 2: Generate a migration

Create a migration with a clear message, such as:

```bash
flask db migrate -m "add recipe reviews"
```

This command should create a new migration file inside the `migrations/versions/` folder.

### Step 3: Inspect the migration file

Open the generated migration file before applying it.

Check that it creates the review table and includes the expected columns:

- rating
- comment
- created_at
- recipe_id
- user_id

Also check that foreign keys are included for the recipe and user relationships.

Do not blindly apply migrations without reading them.

### Step 4: Apply the migration

Apply the migration to your local database:

```bash
flask db upgrade
```

### Step 5: Confirm the database changed

Use one of the following approaches:

- open the database in a database viewer
- use the Flask shell
- run the app and test the form
- inspect the database tables if using SQLite

You should be able to confirm that the new review table exists.

---

## Part 3: Add the Form Class

Add a new form class named `RecipeReviewForm` to `app/forms.py`.

The form should collect:

| Field | Suggested WTForms field | Validation |
|---|---|---|
| `rating` | Integer field or select field | Required, value from 1 to 5 |
| `comment` | Text area field | Required, reasonable length limit |
| `submit` | Submit field | Button text such as `Submit Review` |

### Guidance for rating

You may choose either approach:

1. Use an integer input and validate that the value is between 1 and 5.
2. Use a dropdown/select field with choices 1, 2, 3, 4, and 5.

The dropdown approach is more user-friendly because it prevents many invalid values before the form is even submitted. The integer field approach gives more practice with numeric validation.

### Guidance for comment

The comment should not be empty. It should also have a maximum length so users cannot submit extremely long text.

A reasonable range would be:

- minimum: 5 or 10 characters
- maximum: 300 or 500 characters

Choose a limit that makes sense and apply it consistently in the form and model.

---

## Part 4: Add the Route

Add a new route to `app/routes.py`.

Suggested URL:

```text
/recipes/<recipe_id>/review
```

The exact route may use `<int:recipe_id>` depending on how the existing recipe detail routes are written.

### Required route behavior

The route should:

1. Require the user to be logged in.
2. Find the recipe being reviewed.
3. Show an empty review form on `GET`.
4. Validate submitted form data on `POST`.
5. If the form is invalid, re-render the form with field errors.
6. If the form is valid, create a `RecipeReview` object.
7. Connect the review to the recipe.
8. Connect the review to the current logged-in user.
9. Save the review to the database.
10. Flash a success message.
11. Redirect back to the recipe detail page or recipe list.

### Important design question

Should a user be allowed to review the same recipe more than once?

For this homework, choose one of these approaches:

**Option A: Simpler version**

Allow multiple reviews from the same user for the same recipe.

This is easier and acceptable for this assignment.

**Option B: More realistic version**

Allow only one review per user per recipe.

If you choose this option, your route should check whether the current user already reviewed this recipe. If a review already exists, the route should either:

- redirect with a flash message, or
- update the existing review instead of creating a new one

Option B is a little more challenging. Option A is enough for full credit unless your instructor says otherwise.

---

## Part 5: Add a Link from the Recipe Detail Page

Find the template that displays a single recipe.

Add a link or button that sends the user to the review form.

The link should point to the route you created, passing the current recipe's ID.

Suggested button text:

```text
Write a Review
```

If the app already shows different navigation for logged-in and logged-out users, think about whether this button should be visible to everyone or only logged-in users.

A reasonable design is:

- logged-in users see `Write a Review`
- logged-out users see a message such as `Log in to write a review`

---

## Part 6: Use This Template

Create this file:

```text
templates/recipes/review_form.html
```

Use the template below. You may adjust small wording, but do not redesign the page from scratch.

```html
{% extends "base.html" %}

{% block content %}
<section class="auth-card">
  <h1>Write a Review</h1>
  <p class="muted">
    Share your thoughts about this recipe. Your review will help other users decide what to try.
  </p>

  {% if recipe %}
    <div class="review-recipe-summary">
      <strong>Recipe:</strong> {{ recipe.title }}
    </div>
  {% endif %}

  <form method="POST">
    {{ form.hidden_tag() }}

    <div class="form-group">
      {{ form.rating.label }}
      {{ form.rating(class="form-control") }}
      {% for error in form.rating.errors %}
        <div class="field-error">{{ error }}</div>
      {% endfor %}
    </div>

    <div class="form-group">
      {{ form.comment.label }}
      {{ form.comment(class="form-control", rows="5", placeholder="What did you think of this recipe?") }}
      {% for error in form.comment.errors %}
        <div class="field-error">{{ error }}</div>
      {% endfor %}
    </div>

    {{ form.submit(class="btn btn-primary btn-block") }}
  </form>

  <p class="auth-switch">
    <a href="{{ url_for('main_bp.get_recipe', recipe_id=recipe.id) }}">← Back to recipe</a>
  </p>
</section>

<style>
  .review-recipe-summary {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: .75rem 1rem;
    margin-bottom: 1.25rem;
    color: var(--text);
    font-size: .92rem;
  }

  textarea.form-control {
    min-height: 120px;
    resize: vertical;
  }
</style>
{% endblock %}
```

### Template assumptions

This template assumes your route passes both of these variables into `render_template`:

- `form`
- `recipe`

It also assumes your recipe detail route is named:

```text
main_bp.get_recipe
```

If your project uses a different endpoint name, update the `url_for` call in the template to match your application.

---

## Part 7: Display Reviews on the Recipe Detail Page

After reviews can be saved, update the recipe detail page so users can see existing reviews.

You do not need a complicated design. A simple section is enough.

The recipe detail page should show each review's:

- rating
- comment
- author's username, if available
- created date, if available

You may keep this display simple. The main homework goal is the form flow, not front-end design.

---

## Part 8: Testing Guidance

Add at least two tests.

### Test 1: Login required

Confirm that a logged-out user cannot submit a review.

The exact expected response depends on how Flask-Login is configured in your app. It may redirect to login or return an unauthorized response.

### Test 2: Successful review submission

Create or log in as a user, create a recipe, submit valid review data, and confirm that a review was saved.

### Optional test: Validation failure

Submit invalid data, such as:

- blank comment
- rating outside the allowed range
- non-numeric rating if using an integer field

Confirm the response shows validation errors and does not create a review.

---

## Suggested Work Order

Use this order so you can test one layer at a time:

1. Add the `RecipeReview` model.
2. Generate and inspect the migration.
3. Apply the migration.
4. Add the `RecipeReviewForm` class.
5. Add the review route.
6. Add the review template.
7. Add a `Write a Review` link from the recipe detail page.
8. Submit invalid data and confirm errors show.
9. Submit valid data and confirm the review saves.
10. Display saved reviews on the recipe detail page.
11. Add tests.

---

## Common Mistakes to Watch For

### Forgetting `methods=["GET", "POST"]`

If the route only allows `GET`, the form page may display, but submitting the form will fail.

### Forgetting `form.hidden_tag()`

If CSRF protection is enabled, forms need the hidden CSRF token.

### Redirecting after validation failure

If validation fails, re-render the same template with the same form object. Do not redirect before showing errors.

### Saving raw request data directly

Use the validated form data, not unchecked request values.

### Forgetting to connect the review to the recipe

The review should not just store a rating and comment. It must belong to the recipe being reviewed.

### Forgetting to connect the review to the current user

Since this is a logged-in action, the review should record who wrote it.

### Running `flask db upgrade` before inspecting the migration

Always inspect generated migrations before applying them.

---

## Submission Checklist

Before submitting, confirm that you have:

- [ ] Added `RecipeReview` to `app/models.py`
- [ ] Created a migration for the new model
- [ ] Inspected the generated migration file
- [ ] Applied the migration with `flask db upgrade`
- [ ] Added `RecipeReviewForm` to `app/forms.py`
- [ ] Added a protected review route to `app/routes.py`
- [ ] Created `templates/recipes/review_form.html` using the provided template
- [ ] Added a link to the review form from the recipe detail page
- [ ] Displayed saved reviews on the recipe detail page
- [ ] Tested at least one invalid submission
- [ ] Tested one successful submission
- [ ] Added at least two automated tests

---

## Final Reflection Questions

Answer these briefly in your submission notes or README:

1. What is the difference between the `RecipeReviewForm` and the `RecipeReview` model?
2. Why does the review route need both `GET` and `POST`?
3. What happens when `form.validate_on_submit()` returns `False`?
4. Why should this route require login?
5. What database relationship connects a review to a recipe?
