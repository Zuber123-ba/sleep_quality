const submitBtn = document.getElementById("submitBtn") || document.querySelector("button");
const resultEl = document.getElementById("result");
const adviceEl = document.getElementById("advice") || resultEl;

// ----------------------------------
// RULE-BASED PREDICTION SYSTEM
// ----------------------------------
submitBtn.addEventListener("click", () => {

  const data = {
    sleep_duration: Number(document.getElementById("sleep_duration").value),
    stress_level: Number(document.getElementById("stress_level").value),
    caffeine: Number(document.getElementById("caffeine_intake").value),
    screen_time: Number(document.getElementById("screen_time").value)
  };

  // 🔴 Validation
  if (
    !data.sleep_duration ||
    !data.stress_level ||
    !data.caffeine ||
    !data.screen_time
  ) {
    resultEl.innerHTML = "<p style='color:red'>Please fill all fields</p>";
    return;
  }

  let score = 0;

  // Sleep hours
  if (data.sleep_duration >= 7 && data.sleep_duration <= 9) score += 2;
  else if (data.sleep_duration >= 5) score += 1;

  // Stress
  if (data.stress_level <= 3) score += 2;
  else if (data.stress_level <= 6) score += 1;

  // Caffeine
  if (data.caffeine <= 2) score += 2;
  else if (data.caffeine <= 4) score += 1;

  // Screen time
  if (data.screen_time <= 1) score += 2;
  else if (data.screen_time <= 3) score += 1;

  // Final label
  let label = "";
  if (score >= 7) label = "Best";
  else if (score >= 4) label = "Good";
  else label = "Bad";

  // ✅ SHOW RESULT
  resultEl.innerHTML = `
    <div class="badge ${label.toLowerCase()}">${label}</div>
  `;

  // -------------------------------
  // ADVICE SYSTEM
  // -------------------------------
  const tips = [];

  if (data.sleep_duration < 6)
    tips.push("Try to sleep at least 7–8 hours daily.");

  if (data.stress_level > 6)
    tips.push("Practice meditation or deep breathing to reduce stress.");

  if (data.caffeine > 3)
    tips.push("Reduce caffeine intake, especially after 6 PM.");

  if (data.screen_time > 4)
    tips.push("Reduce screen usage at least 1 hour before bed.");

  if (label === "Bad")
    tips.push("Your sleep quality is poor — improve your routine.");

  if (label === "Good")
    tips.push("Good sleep! Small improvements can make it even better.");

  if (label === "Best")
    tips.push("Excellent sleep habits! Keep it up.");

  adviceEl.style.display = "block";
  adviceEl.innerHTML = tips.map(t => "• " + t).join("<br>");
});
