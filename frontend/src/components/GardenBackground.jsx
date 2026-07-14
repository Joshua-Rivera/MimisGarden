import { forwardRef } from "react";
import cleanTree from "../assets/cleantree.png";
import mountainBackground from "../assets/mountainbg.png";

const windLeaves = Array.from({ length: 8 });
const fallingLeaves = Array.from({ length: 6 });

const GardenBackground = forwardRef(function GardenBackground({ isActive = true }, ref) {
    return (
        <div
            ref={ref}
            className={`site-garden-background${isActive ? " garden-background-active" : ""}`}
            aria-hidden="true"
        >
            <div className="garden-scene-shell">
                <img src={mountainBackground} alt="" className="mountain-background" />

                {isActive && (
                    <div className="wind-leaves">
                        {windLeaves.map((_, index) => (
                            <span className="animated-leaf" key={index} />
                        ))}
                    </div>
                )}

                <div className="tree-layer">
                    <img src={cleanTree} alt="" className="tree-image tree-image-sway" />
                    {isActive && (
                        <div className="falling-leaves">
                            {fallingLeaves.map((_, index) => (
                                <span className="animated-leaf" key={index} />
                            ))}
                        </div>
                    )}
                </div>

                <div className="scene-vignette" />
            </div>
        </div>
    );
});

export default GardenBackground;
