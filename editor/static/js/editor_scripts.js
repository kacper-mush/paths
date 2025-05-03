class PointManager {
    POINT_RADIUS = {
        DEFAULT: 5,
        HOVER: 10,
        SELECTED: 13,
        HITBOX: 20
    };

    lineLayer = document.getElementById('line-svg-layer');
    pointLayer = document.getElementById('point-svg-layer');
    pointForm = document.getElementById("point-form");
    pointsInput = document.getElementById('points-input'); // to send to backend
    backgroundImage = document.getElementById('background-image');

    constructor() {
        this.selectedPoint = null;
        this.pointCords = [];
        this.initializePoints(window.pointCords);
        this.setupEventListeners();
        this.uiManager = new UIManager(this)
    }

    initializePoints(pointCords) {
        this.pointLayer.innerHTML = '';
        this.lineLayer.innerHTML = '';

        pointCords.forEach((cords) => {
            this.addPointToPath(cords);
        });
    }

    setupEventListeners() {
        this.pointLayer.addEventListener('mousedown', this.handleMouseDown.bind(this));
        this.pointLayer.addEventListener('mousemove', this.handleMouseMove.bind(this));
        this.pointLayer.addEventListener('mouseup', this.handleMouseUp.bind(this));
       
        this.pointForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.pointsInput.value = JSON.stringify(this.pointCords);
            e.target.submit();
        });

        window.addEventListener('resize', this.repositionPath.bind(this));
    }

    getScale() {
        const rect = this.backgroundImage.getBoundingClientRect();
        return {
            x: rect.width / this.backgroundImage.naturalWidth,
            y: rect.height / this.backgroundImage.naturalHeight
        };
    }

    getMousePosition(event) {
        const rect = this.backgroundImage.getBoundingClientRect();
        const scale = this.getScale();

        return {
            x: Math.round((event.clientX - rect.left) / scale.x),
            y: Math.round((event.clientY - rect.top) / scale.y)
        };
    }

    getPointCords() {
        return this.pointCords;
    }

    animatePoint(point, radius) {
        const visual = point.querySelector('.point-visual');
        gsap.to(visual, { attr: { r: radius }, duration: 0.2 });
    }

    handleMouseDown(event) {
        // Find the point under the mouse
        var point = event.target.closest('.point');

        if (point == null) {
            // If no point is found, create a new one
            const cords = this.getMousePosition(event);
            point = this.addPointToPath(cords);
            this.uiManager.addPointItem(cords);
        }
        
        // Select the either existing or newly created point to be dragged
        this.selectedPoint = point;
        this.animatePoint(point, this.POINT_RADIUS.SELECTED);
    }

    handleMouseMove(event) {
        if (this.selectedPoint) {
            const cords = this.getMousePosition(event);
            const index = parseInt(this.selectedPoint.dataset.index);
            // Set the new position of the point
            this.pointCords[index] = cords;
            // Update the position of the point in the SVG
            this.repositionPoint(this.selectedPoint, cords);
            this.uiManager.updatePointItem(cords, index);
        }
    }

    handleMouseUp() {
        if (this.selectedPoint) {
            this.animatePoint(this.selectedPoint, this.POINT_RADIUS.HOVER);
            this.selectedPoint = null;
        }
    }

    repositionPoint(point) {
        const index = parseInt(point.dataset.index);
        const cords = this.pointCords[index];

        const scale = this.getScale();
        const hitbox = point.querySelector('.point-hitbox');
        const visual = point.querySelector('.point-visual');

        hitbox.setAttribute('cx', cords.x * scale.x);
        hitbox.setAttribute('cy', cords.y * scale.y);
        visual.setAttribute('cx', cords.x * scale.x);
        visual.setAttribute('cy', cords.y * scale.y);

        // Update the lines connected to this point
        if (index > 0) {
            const previousLine = this.lineLayer.querySelector(`.line[data-index="${index - 1}"]`);
            previousLine.setAttribute('x2', cords.x * scale.x);
            previousLine.setAttribute('y2', cords.y * scale.y);
        }
        if (index < this.pointCords.length - 1) {
            const nextLine = this.lineLayer.querySelector(`.line[data-index="${index}"]`);
            nextLine.setAttribute('x1', cords.x * scale.x);
            nextLine.setAttribute('y1', cords.y * scale.y);
        }
    }

    repositionPath() {
        // Reposition all points
        this.pointLayer.querySelectorAll('.point').forEach(point => {
            this.repositionPoint(point);
        });
    }

    // Add a new point to the path and create a line to the previous point
    // Returns the new point element
    addPointToPath(cords) {
        const index = this.pointCords.length;
        this.pointCords.push(cords);
        const newPoint = this.createPoint(cords, index);
        this.pointLayer.appendChild(newPoint);
        if (index > 0) {
            this.createLine(this.pointCords[index - 1], cords, index - 1);
        }

        return newPoint;
    }

    createPoint(cords, index) {
        const scale = this.getScale();
        const scaledX = cords.x * scale.x;
        const scaledY = cords.y * scale.y;

        const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        group.classList.add('point');
        group.dataset.index = index;

        const hitbox = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        hitbox.classList.add('point-hitbox');
        hitbox.setAttribute('cx', scaledX);
        hitbox.setAttribute('cy', scaledY);
        hitbox.setAttribute('r', this.POINT_RADIUS.HITBOX);
        

        const visual = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        visual.classList.add('point-visual');
        visual.setAttribute('cx', scaledX);
        visual.setAttribute('cy', scaledY);
        visual.setAttribute('r', this.POINT_RADIUS.DEFAULT);

        hitbox.addEventListener('mouseenter', () => {
            this.animatePoint(group, this.POINT_RADIUS.HOVER);
        });

        hitbox.addEventListener('mouseleave', () => {
            this.animatePoint(group, this.POINT_RADIUS.DEFAULT);
        });
    
        group.appendChild(hitbox);
        group.appendChild(visual);
        
        return group;
    }

    createLine(cords1, cords2, index) {
        const scale = this.getScale();
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.classList.add('line');
        line.setAttribute('x1', cords1.x * scale.x);
        line.setAttribute('y1', cords1.y * scale.y);
        line.setAttribute('x2', cords2.x * scale.x);
        line.setAttribute('y2', cords2.y * scale.y);
        line.dataset.index = index;
        this.lineLayer.appendChild(line);
    }

    highlightPoint(index) {
        const point = this.pointLayer.querySelector(`.point[data-index="${index}"]`);
        point.classList.add('highlighted');
        this.animatePoint(point, this.POINT_RADIUS.HOVER);
    }

    unhighlightPoint(index) {
        const point = this.pointLayer.querySelector(`.point[data-index="${index}"]`);
        point.classList.remove('highlighted');
        this.animatePoint(point, this.POINT_RADIUS.DEFAULT);
    }

    deletePoint(index) {
        // Remove the point cord
        this.pointCords.splice(index, 1);
        
        this.pointLayer.querySelectorAll('.point').forEach(point => {
            if (point.dataset.index == index) {
                // Remove the point from the SVG
                point.remove();
            }
            if (point.dataset.index > index) {
                // Adjust the index of the points after the deleted point
                point.dataset.index = point.dataset.index - 1;
            }
        });

        this.lineLayer.querySelectorAll('.line').forEach(line => {
            if (line.dataset.index == index - 1) {
                if (index < this.pointCords.length) {
                    // Update the line to connect to the next point
                    line.setAttribute('x2', this.pointCords[index].x * this.getScale().x);
                    line.setAttribute('y2', this.pointCords[index].y * this.getScale().y);
                } else {
                    // Remove the line if it's the last point
                    line.remove();
                }
            }

            // Remove the line coming out from the deleted point
            if (line.dataset.index == index) {
                line.remove();
            }
            if (line.dataset.index > index) {
                // Adjust the index of the lines after the deleted line
                line.dataset.index = line.dataset.index - 1;
            }
        });

        this.uiManager.updatePointList();
    }
}


class UIManager {
    constructor(pointManager) {
        this.pointManager = pointManager;
        this.overlay = document.getElementById('overlay');
        this.toggleButton = document.getElementById('toggleUI');
        this.overlayTab = document.getElementById('overlayTab');
        this.setupEventListeners();
        this.updatePointList();
    }

    setupEventListeners() {
        this.toggleButton.addEventListener('click', () => {
            this.overlay.classList.toggle('overlay-hidden');
            this.toggleButton.textContent = this.overlay.classList.contains('overlay-hidden') ? 'Show' : 'Hide';
            this.overlayTab.style.display = this.overlay.classList.contains('overlay-hidden') ? 'block' : 'none';
        });

        this.overlayTab.addEventListener('click', () => {
            this.overlay.classList.remove('overlay-hidden');
            this.toggleButton.textContent = 'Hide';
            this.overlayTab.style.display = 'none';
        });

        document.querySelector('.dashboard-button').addEventListener('click', function() {
            window.location.href = this.dataset.url;
        });
    }

    createPointItem(cords, index) {
        const template = document.getElementById('point-item-template');
        const clone = template.content.cloneNode(true);
        const item = clone.querySelector('.point-item');
        const label = clone.querySelector('.point-label');
        const deleteButton = clone.querySelector('.delete-point');
    
        item.dataset.index = index;
        label.textContent = `Point ${index + 1}: (${cords.x}, ${cords.y})`;
        deleteButton.dataset.index = index;
    
        // Hover events
        item.addEventListener('mouseenter', () => this.highlightPointItem(index));
        item.addEventListener('mouseleave', () => this.unhighlightPointItem(index));
        deleteButton.addEventListener('click', this.deleteButtonAction.bind(this));
        return clone;
    }

    updatePointList() {
        const pointList = document.getElementById('point-list');
        pointList.innerHTML = '';

        this.pointManager.getPointCords().forEach((cords, index) => {
            pointList.appendChild(this.createPointItem(cords, index));
        });

    }

    addPointItem(cords) {
        const pointList = document.getElementById('point-list');
        const index = this.pointManager.getPointCords().length - 1;
        const pointItem = this.createPointItem(cords, index);
        pointList.appendChild(pointItem);
    }

    // Update the point item coordinate display
    updatePointItem(cords, index) {
        const pointList = document.getElementById('point-list');
        const pointItem = pointList.querySelector(`.point-item[data-index="${index}"]`);
        const label = pointItem.querySelector('.point-label');
        label.textContent = `Point ${index + 1}: (${cords.x}, ${cords.y})`;
    }

    deleteButtonAction(event) {
        const index = parseInt(event.target.dataset.index);
        this.pointManager.deletePoint(index);
        this.updatePointList();
    }

    highlightPointItem(index) {
        // Highlight the point item
        const pointItems = document.querySelectorAll('.point-item');
        pointItems[index].classList.add('highlighted');

        // Highlight the corresponding point
        this.pointManager.highlightPoint(index);
    }

    unhighlightPointItem(index) {
        // Unhighlight the point item
        const pointItems = document.querySelectorAll('.point-item');
        pointItems[index].classList.remove('highlighted');

        // Unhighlight the corresponding point
        this.pointManager.unhighlightPoint(index);
    }
}

// Initialize the point manager
new PointManager();
