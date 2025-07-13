document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form');
  const wlInput = document.querySelector('input[name="wl"]');
  const travelDateInput = document.querySelector('input[name="journey_date"], input[name="travel_date"]');

  if (form && wlInput && travelDateInput) {
    form.addEventListener('submit', function (e) {
      const wlValue = parseInt(wlInput.value);
      const today = new Date();
      const travelDate = new Date(travelDateInput.value);
      const gapInDays = Math.floor((travelDate - today) / (1000 * 60 * 60 * 24));

      if (isNaN(wlValue) || wlValue > 150) {
        alert(" Waiting List should not be greater than 150.");
        e.preventDefault();
        return;
      }

      if (gapInDays < 0) {
        alert(" Journey date must be after today's date.");
        e.preventDefault();
        return;
      }

      if (gapInDays > 60) {
        alert(" Journey date cannot be more than 60 days from today.");
        e.preventDefault();
        return;
      }
    });
  }
});
