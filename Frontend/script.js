document.addEventListener("DOMContentLoaded", () => {
  const products = [];

  const els = {
    productName: document.getElementById("productName"),
    productPrice: document.getElementById("productPrice"),
    purchaseFreq: document.getElementById("purchaseFreq"),
    lifespan: document.getElementById("lifespan"),
    margin: document.getElementById("margin"),
    marketingBudget: document.getElementById("marketingBudget"),
    cac: document.getElementById("cac"),
    addProductBtn: document.getElementById("addProductBtn"),
    recalcBtn: document.getElementById("recalcBtn"),
    productsTableBody: document.getElementById("productsTableBody"),
    cliOutput: document.getElementById("cliOutput"),
    customersPerMonth: document.getElementById("customersPerMonth"),
    avgClv: document.getElementById("avgClv"),
    clvCacRatio: document.getElementById("clvCacRatio"),
  };

  function addCliLine(text) {
    const line = document.createElement("div");
    line.className = "cli-line";
    line.innerHTML = `<span class="cli-prompt">$</span> ${text}`;
    els.cliOutput.appendChild(line);
    els.cliOutput.scrollTop = els.cliOutput.scrollHeight;
  }

  function parseNumber(el) {
    const value = parseFloat(el.value);
    return isNaN(value) ? 0 : value;
  }

  function computeClv(price, freq, lifespan, marginPct) {
    // Simple CLV model: CLV = Avg Order Value * Orders/Year * Lifespan (yrs) * Margin
    const margin = marginPct / 100;
    return price * freq * lifespan * margin;
  }

  function refreshTable() {
    els.productsTableBody.innerHTML = "";

    products.forEach((p) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${p.name}</td>
        <td>${p.price.toFixed(0)}</td>
        <td>${p.freq.toFixed(1)}</td>
        <td>${p.lifespan.toFixed(1)}</td>
        <td>${p.margin.toFixed(0)}</td>
        <td>${p.clv.toFixed(0)}</td>
      `;
      els.productsTableBody.appendChild(tr);
    });
  }

  function refreshSummary() {
    const budget = parseNumber(els.marketingBudget);
    const cac = parseNumber(els.cac);

    let customersPerMonth = 0;
    if (budget > 0 && cac > 0) {
      customersPerMonth = budget / cac;
    }

    let avgClv = 0;
    if (products.length > 0) {
      const totalClv = products.reduce((sum, p) => sum + p.clv, 0);
      avgClv = totalClv / products.length;
    }

    let ratio = 0;
    if (cac > 0 && avgClv > 0) {
      ratio = avgClv / cac;
    }

    els.customersPerMonth.textContent = customersPerMonth.toFixed(1);
    els.avgClv.textContent = avgClv.toFixed(0);
    els.clvCacRatio.textContent = ratio.toFixed(2);
  }

  function handleAddProduct() {
    const name = els.productName.value.trim() || "Unnamed";
    const price = parseNumber(els.productPrice);
    const freq = parseNumber(els.purchaseFreq);
    const lifespan = parseNumber(els.lifespan);
    const margin = parseNumber(els.margin) || 0;

    if (!price || !freq || !lifespan || !margin) {
      addCliLine(
        "warn: please enter price, orders/year, lifespan, and margin% (all > 0) to add a product."
      );
      return;
    }

    const clv = computeClv(price, freq, lifespan, margin);

    const product = { name, price, freq, lifespan, margin, clv };
    products.push(product);

    addCliLine(
      `product:add name="${name}" price=${price} freq=${freq} lifespan=${lifespan}yrs margin=${margin}% => CLV≈₹${clv.toFixed(
        0
      )}`
    );

    refreshTable();
    refreshSummary();

    els.productName.value = "";
    els.productPrice.value = "";
    els.purchaseFreq.value = "";
    els.lifespan.value = "";
    els.margin.value = "";
  }

  function handleRecalc() {
    refreshSummary();
    const budget = parseNumber(els.marketingBudget);
    const cac = parseNumber(els.cac);

    addCliLine(
      `budget:calc marketing=₹${budget.toFixed(0)} cac=₹${cac.toFixed(
        0
      )} -> customers/month≈${els.customersPerMonth.textContent}, avg CLV≈₹${
        els.avgClv.textContent
      }, CLV:CAC≈${els.clvCacRatio.textContent}`
    );
  }

  // Event listeners
  els.addProductBtn.addEventListener("click", handleAddProduct);
  els.recalcBtn.addEventListener("click", handleRecalc);

  // Initial CLI intro
  addCliLine("welcome to Product Finance CLI demo.");
  addCliLine("tip: add products on the left, then set marketing budget & CAC.");
});
