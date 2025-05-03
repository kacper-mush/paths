// Same as in editor_scripts.js but trimmed down

class PointManager {
    POINT_RADIUS = {
        DEFAULT: 5,
        HITBOX: 20
    };

    lineLayer = document.getElementById('line-svg-layer');
    pointLayer = document.getElementById('point-svg-layer');
    backgroundImage = document.getElementById('background-image');

    constructor() {
        this.selectedPoint = null;
        this.pointCords = [];
        this.initializePoints(window.pointCords);
        this.setupEventListeners();
    }

    initializePoints(pointCords) {
        this.pointLayer.innerHTML = '';
        this.lineLayer.innerHTML = '';

        pointCords.forEach((cords) => {
            this.addPointToPath(cords);
        });
    }

    setupEventListeners() {
        window.addEventListener('resize', this.repositionPath.bind(this));
    }

    getScale() {
        const rect = this.backgroundImage.getBoundingClientRect();
        return {
            x: rect.width / this.backgroundImage.naturalWidth,
            y: rect.height / this.backgroundImage.naturalHeight
        };
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
}

// Initialize the point manager
new PointManager();
