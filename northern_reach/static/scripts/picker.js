window.onload = function () {
	const picker = new Litepicker({
		element: document.getElementById("litepicker"),
		elementEnd: document.getElementById("litepicker2"),
		startDate: new Date(),
		singleMode: false,
		numberOfMonths: 2,
		numberOfColumns: 2,
		setup: (picker) => {
			picker.on("selected", (date1, date2) => {
				console.log(date1, date2);
				document.getElementById("start-date").value =
					date1.toJSDate().toISOString().split("T")[0] ?? "";
				document.getElementById("end-date").value =
					date2.toJSDate().toISOString().split("T")[0] ?? "";
				filterInteractions();
			});
		},
	});
};
