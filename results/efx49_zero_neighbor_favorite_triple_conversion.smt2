; benchmark generated from python API
(set-info :status unknown)
(declare-fun F () Real)
(declare-fun h () Real)
(declare-fun ell () Real)
(declare-fun x () Real)
(declare-fun y () Real)
(declare-fun p1 () Real)
(declare-fun p2 () Real)
(declare-fun q1 () Real)
(declare-fun q2 () Real)
(assert
 (> F 0.0))
(assert
 (> h 0.0))
(assert
 (> ell 0.0))
(assert
 (> x 0.0))
(assert
 (> y 0.0))
(assert
 (> p1 0.0))
(assert
 (> p2 0.0))
(assert
 (> q1 0.0))
(assert
 (> q2 0.0))
(assert
 (> F h))
(assert
 (> F ell))
(assert
 (> F x))
(assert
 (> F y))
(assert
 (> F p1))
(assert
 (> F p2))
(assert
 (> F q1))
(assert
 (> F q2))
(assert
 (>= h ell))
(assert
 (let ((?x120 (+ F h)))
 (let ((?x16 (+ x y)))
 (< ?x16 ?x120))))
(assert
 (let ((?x16 (+ x y)))
 (let ((?x122 (+ ?x16 ell)))
 (>= ?x122 F))))
(assert
 (let ((?x14 (+ p1 p2)))
 (>= ?x14 F)))
(assert
 (let ((?x16 (+ x y)))
 (let ((?x14 (+ p1 p2)))
 (>= ?x14 ?x16))))
(assert
 (let ((?x135 (+ ell x)))
 (let ((?x14 (+ p1 p2)))
 (>= ?x14 ?x135))))
(assert
 (let ((?x137 (+ ell y)))
 (let ((?x14 (+ p1 p2)))
 (>= ?x14 ?x137))))
(assert
 (let ((?x15 (+ q1 q2)))
 (>= ?x15 F)))
(assert
 (let ((?x16 (+ x y)))
 (let ((?x15 (+ q1 q2)))
 (>= ?x15 ?x16))))
(assert
 (let ((?x135 (+ ell x)))
 (let ((?x15 (+ q1 q2)))
 (>= ?x15 ?x135))))
(assert
 (let ((?x137 (+ ell y)))
 (let ((?x15 (+ q1 q2)))
 (>= ?x15 ?x137))))
(assert
 (or (< (+ F h) F) (< (+ F h) h) (< (+ F h) (+ x y)) (< (+ F h) (+ ell x)) (< (+ F h) (+ ell y)) (< (+ F h) p1) (< (+ F h) p2) (< (+ F h) q1) (< (+ F h) q2) (< (+ (+ x y) ell) F) (< (+ (+ x y) ell) h) (< (+ (+ x y) ell) (+ x y)) (< (+ (+ x y) ell) (+ ell x)) (< (+ (+ x y) ell) (+ ell y)) (< (+ (+ x y) ell) p1) (< (+ (+ x y) ell) p2) (< (+ (+ x y) ell) q1) (< (+ (+ x y) ell) q2) (< (+ p1 p2) F) (< (+ p1 p2) h) (< (+ p1 p2) (+ x y)) (< (+ p1 p2) (+ ell x)) (< (+ p1 p2) (+ ell y)) (< (+ p1 p2) p1) (< (+ p1 p2) p2) (< (+ p1 p2) q1) (< (+ p1 p2) q2) (< (+ q1 q2) F) (< (+ q1 q2) h) (< (+ q1 q2) (+ x y)) (< (+ q1 q2) (+ ell x)) (< (+ q1 q2) (+ ell y)) (< (+ q1 q2) p1) (< (+ q1 q2) p2) (< (+ q1 q2) q1) (< (+ q1 q2) q2)))
(check-sat)
