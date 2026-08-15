const state = new Map();
const currency = new Intl.NumberFormat(document.documentElement.lang || "en", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

const menuButton = document.querySelector("[data-testid='mobile-menu-toggle']");
const navigation = document.querySelector("#primary-navigation");
const search = document.querySelector("[data-testid='experience-search']");
const cards = [...document.querySelectorAll("[data-testid='experience-card']")];
const resultStatus = document.querySelector("[data-result-status]");
const planItems = document.querySelector("[data-plan-items]");
const planTotal = document.querySelector("[data-plan-total]");
const planCounts = document.querySelectorAll("[data-plan-count]");
const emptyPlan = document.querySelector("[data-empty-plan]");
const reviewButton = document.querySelector("[data-review-plan]");
const clearButton = document.querySelector("[data-clear-plan]");
const dialog = document.querySelector("[data-booking-dialog]");
const bookingForm = document.querySelector("[data-booking-form]");
const confirmation = document.querySelector("[data-confirmation]");
const formError = document.querySelector("[data-form-error]");

function setMenu(open) {
  menuButton.setAttribute("aria-expanded", String(open));
  navigation.classList.toggle("primary-navigation--open", open);
}

menuButton.addEventListener("click", () => {
  setMenu(menuButton.getAttribute("aria-expanded") !== "true");
});

navigation.addEventListener("click", (event) => {
  if (event.target.closest("a")) setMenu(false);
});

search.addEventListener("input", () => {
  const query = search.value.trim().toLocaleLowerCase();
  let visible = 0;
  cards.forEach((card) => {
    const matches = card.dataset.search.toLocaleLowerCase().includes(query);
    card.hidden = !matches;
    if (matches) visible += 1;
  });
  resultStatus.textContent = `${visible} ${visible === 1 ? "experience" : "experiences"} available`;
});

document.querySelectorAll("[data-price]").forEach((element) => {
  element.textContent = currency.format(Number(element.dataset.price));
});

function renderPlan() {
  planItems.replaceChildren();
  let total = 0;
  state.forEach((experience, id) => {
    total += experience.price;
    const item = document.createElement("li");
    const name = document.createElement("span");
    const remove = document.createElement("button");
    name.textContent = experience.name;
    remove.type = "button";
    remove.textContent = "Remove";
    remove.dataset.removeExperience = id;
    remove.setAttribute("aria-label", `Remove ${experience.name}`);
    item.append(name, remove);
    planItems.append(item);
  });

  const count = state.size;
  planCounts.forEach((element) => {
    element.textContent = String(count);
  });
  planTotal.textContent = currency.format(total);
  emptyPlan.hidden = count > 0;
  reviewButton.disabled = count === 0;
  clearButton.disabled = count === 0;

  document.querySelectorAll("[data-add-experience]").forEach((button) => {
    const selected = state.has(button.dataset.addExperience);
    button.disabled = selected;
    button.textContent = selected ? "Added" : "Add to plan";
  });
}

document.addEventListener("click", (event) => {
  const addButton = event.target.closest("[data-add-experience]");
  if (addButton) {
    state.set(addButton.dataset.addExperience, {
      name: addButton.dataset.experienceName,
      price: Number(addButton.dataset.experiencePrice),
    });
    renderPlan();
  }

  const removeButton = event.target.closest("[data-remove-experience]");
  if (removeButton) {
    state.delete(removeButton.dataset.removeExperience);
    renderPlan();
  }
});

clearButton.addEventListener("click", () => {
  state.clear();
  renderPlan();
});

reviewButton.addEventListener("click", () => {
  bookingForm.hidden = false;
  confirmation.hidden = true;
  formError.hidden = true;
  dialog.showModal();
  bookingForm.elements.traveler_name.focus();
});

document.querySelector("[data-close-dialog]").addEventListener("click", () => dialog.close());
document.querySelector("[data-close-confirmation]").addEventListener("click", () => dialog.close());

bookingForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  formError.hidden = true;
  const formData = new FormData(bookingForm);
  const response = await fetch("/api/bookings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      experience_ids: [...state.keys()],
      traveler_name: formData.get("traveler_name"),
      traveler_email: formData.get("traveler_email"),
    }),
  });

  if (!response.ok) {
    formError.textContent = "The plan could not be confirmed. Check the traveler details.";
    formError.hidden = false;
    return;
  }

  const booking = await response.json();
  document.querySelector("[data-booking-id]").textContent = booking.booking_id;
  bookingForm.hidden = true;
  confirmation.hidden = false;
});

renderPlan();
